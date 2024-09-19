"""Routers that can be accessed only in test mode"""

from fastapi import APIRouter, Depends
from loguru import logger

import utils.auth
from config import config
from utils.response import ErrorCodes, ErrorResponse, SuccessfulResponse
from db import methods
from db.client import client
from db.types import types, RS, RQ


router = APIRouter()


@router.post("/cleanup", response_model=SuccessfulResponse[None])
async def cleanup():
    db = client.get_database(config.database.name)
    for collection_name in db.list_collection_names():
        db.get_collection(collection_name).delete_many({})
    logger.warning("CLEARED ALL COLLECTIONS")
    return


@router.post("/signup", response_model=SuccessfulResponse[RS.test.signup])
async def signup(request: RQ.test.signup):
    hashed_password = utils.auth.hash_password(request.password)

    inserted_user_id = methods.users.insert_user(
        types.UserWithoutID(
            email=request.email,
            hashed_password=hashed_password,
            first_name=request.first_name,
        )
    )

    if inserted_user_id is None:
        raise ErrorResponse(
            code=ErrorCodes.EMAIL_ALREADY_TAKEN,
        )

    return utils.auth.create_jwt_pair_by_user_id(inserted_user_id)


@router.post(
    "/organizations/create",
    response_model=SuccessfulResponse[RS.test.organizations.create],
)
async def create_organization(
    request: RQ.test.organizations.create,
    current_user: types.User = Depends(utils.auth.get_current_user),
):
    inserted_id = methods.organizations.insert_organization(
        types.OrganizationWithoutID(name=request.name, members=[types.Member(id=current_user.id)])
    )

    return RS.test.organizations.create(members=[types.Member(id=current_user.id)], name=request.name, _id=inserted_id)


@router.post("/organizations/invite", response_model=SuccessfulResponse[None])
async def invite_user_to_organization(
    request: RQ.test.organizations.invite,
    current_user: types.User = Depends(utils.auth.get_current_user),
):
    with client.start_session() as session:
        with session.start_transaction():
            if not methods.organizations.check_existence(request.organization_id, session):
                raise ErrorResponse(code=ErrorCodes.ENTITY_NOT_FOUND, message="Organization not found")

            if (methods.users.get(request.user_id), session) is None:
                raise ErrorResponse(code=ErrorCodes.ENTITY_NOT_FOUND, message="User not found")

            if not methods.organizations.is_user_in_organization(current_user.id, request.organization_id, session):
                raise ErrorResponse(
                    code=ErrorCodes.ACCESS_DENIED,
                    message="You are not a member of this organization",
                )

            methods.organizations.add_member(request.organization_id, types.Member(id=request.user_id), session)
