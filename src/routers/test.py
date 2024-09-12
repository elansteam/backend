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

    inserted_user_id = methods.users.insert_user_with_id(
        types.UserWithoutID(
            email=request.email,
            hashed_password=hashed_password,
            first_name=request.first_name
        )
    )

    if inserted_user_id is None:
        raise ErrorResponse(
            code=ErrorCodes.EMAIL_ALREADY_TAKEN,
        )

    return utils.auth.create_jwt_pair_by_user_id(inserted_user_id)

@router.post("/organizations/create", response_model=SuccessfulResponse[RS.test.organizations.create])
async def create_organization(
    request: RQ.test.organizations.create, current_user: types.User = Depends(utils.auth.get_current_user)
):
    inserted_id = methods.organizations.insert_organization_with_id(types.OrganizationWithoutID(
        name=request.name,
        members=[types.Member(id=current_user.id)]
    ))

    return RS.test.organizations.create(
        members=[types.Member(id=current_user.id)],
        name=request.name,
        _id=inserted_id
    )

@router.post("/organizations/invite", response_model=SuccessfulResponse[None])
async def invite_user_to_organization(
    request: RQ.test.organizations.invite, current_user: types.User = Depends(utils.auth.get_current_user)
):
    if (organization := methods.organizations.get(request.organization_id)) is None:
        raise ErrorResponse(code=ErrorCodes.ENTITY_NOT_FOUND, message="Organization not found")

    if (user := methods.users.get(request.user_id)) is None:
        raise ErrorResponse(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            message="User not found"
        )

    if not any(member.id == current_user.id for member in organization.members):
        raise ErrorResponse(
            code=ErrorCodes.ACCESS_DENIED,
            message="User is already a member of this organization"
        )

    if any(member.id == user.id for member in organization.members):
        return

    methods.organizations.add_member(
        organization.id,
        types.Member(id=request.user_id)
    )
