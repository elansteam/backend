"""Routers that can be accessed only in test mode"""

from fastapi import APIRouter, Depends
from loguru import logger

import utils.auth
from config import config
from utils.response import ErrorCodes, ErrorResponse, SuccessfulResponse
from db import methods
from db.client import client
from src import types
from src.types import RQ, RS


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
    inserted_user_id = methods.insert_user(
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
    inserted_id = methods.insert_organization(types.OrganizationWithoutID(name=request.name))
    methods.insert_member_to_organization(types.Member(object_id=current_user.id, target_id=inserted_id))
    return types.Organization(id=inserted_id, name=request.name)


@router.post("/organizations/invite", response_model=SuccessfulResponse[None])
async def invite_user_to_organization(
    request: RQ.test.organizations.invite,
    current_user: types.User = Depends(utils.auth.get_current_user),
):
    if not methods.check_organization_existence(request.organization_id):
        raise ErrorResponse(code=ErrorCodes.NOT_FOUND, message="Organization not found")

    if not methods.check_user_existence(request.user_id):
        raise ErrorResponse(code=ErrorCodes.NOT_FOUND, message="User not found")

    if not methods.is_user_in_organization(current_user.id, request.organization_id):
        raise ErrorResponse(code=ErrorCodes.ACCESS_DENIED, message="You are not a member of this organization")

    is_member_inserted = methods.insert_member_to_organization(
        types.Member(object_id=request.user_id, target_id=request.organization_id)
    )

    if not is_member_inserted:
        raise ErrorResponse(code=ErrorCodes.USER_ALREADY_MEMBER, message="User already in organization")
