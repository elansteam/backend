from fastapi import APIRouter
from fastapi import status as http_status

import utils.auth
from utils.response import SuccessfulResponse, ErrorCodes, ErrorResponse
from db import methods
from db import types
from db.types import requests as RQ, responses as RS


router = APIRouter()


@router.post("/signup", response_model=SuccessfulResponse[RS.AuthSignup])
async def signup(
    request: RQ.AuthSignup
):
    hashed_password = utils.auth.hash_password(request.password)

    inserted_user_id = methods.users.insert_user_with_id(
        types.user.UserWithoutID(
            email=request.email,
            hashed_password=hashed_password,
            first_name=request.first_name
        )
    )

    if inserted_user_id is None:
        raise ErrorResponse(
            code=ErrorCodes.NAME_ALREADY_TAKEN,
            message="There is user with identical email"
        )

    return utils.auth.create_jwt_pair_by_user_id(inserted_user_id)

@router.post("/signin", response_model=SuccessfulResponse[RS.AuthSignin])
async def signin(
    siginin_input: RQ.AuthSignin
):
    user: types.user.User | None = None
    if siginin_input.id:
        user = methods.users.get(siginin_input.id)
    elif siginin_input.domain:
        entity = methods.domains.resolve_entity(siginin_input.domain)
        if entity and entity.target_type == "user":
            user = methods.users.get(entity.target_id)
    elif siginin_input.email:
        user = methods.users.get_by_email(siginin_input.email)

    if user is None:
        raise ErrorResponse(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            http_status_code=http_status.HTTP_404_NOT_FOUND,
            message="User not found"
        )

    if not utils.auth.verify_password(siginin_input.password, user.hashed_password):
        raise ErrorResponse(
            code=ErrorCodes.ACCESS_DENIED,
            http_status_code=http_status.HTTP_403_FORBIDDEN,
            message="Incorrect password"
        )

    return utils.auth.create_jwt_pair_by_user_id(user.id)
