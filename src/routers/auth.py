from fastapi import APIRouter, Depends
from fastapi import status as http_status

import utils.auth
from utils.auth import (
    service_auth,
    get_current_user_by_refresh_token
)
from utils.response import SuccessfulResponse, ErrorCodes, ErrorResponse
from db import methods
from db import types
from db.types import requests as RQ, responses as RS
from db.types.requests import RQ
from db.types.responses import RS


router = APIRouter()


@router.post("/signup", response_model=SuccessfulResponse[RS.auth.signup])
async def signup(request: RQ.auth.signup, _=Depends(service_auth)):
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
            code=ErrorCodes.EMAIL_ALREADY_TAKEN,
        )

    return utils.auth.create_jwt_pair_by_user_id(inserted_user_id)

@router.post("/signin", response_model=SuccessfulResponse[RS.auth.signin])
async def signin(request: RQ.auth.signin):
    user: types.user.User | None = None
    if request.id:
        user = methods.users.get(request.id)
    elif request.domain:
        entity = methods.domains.resolve_entity(request.domain)
        if entity and entity.target_type == "user":
            user = methods.users.get(entity.target_id)
    elif request.email:
        user = methods.users.get_by_email(request.email)

    if user is None:
        raise ErrorResponse(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            http_status_code=http_status.HTTP_404_NOT_FOUND,
            message="User not found"
        )

    if not utils.auth.verify_password(request.password, user.hashed_password):
        raise ErrorResponse(
            code=ErrorCodes.ACCESS_DENIED,
            http_status_code=http_status.HTTP_403_FORBIDDEN,
            message="Incorrect password"
        )

    return utils.auth.create_jwt_pair_by_user_id(user.id)

@router.get("/refresh", response_model=SuccessfulResponse[RS.auth.refresh])
async def refresh(current_user: types.user.User = Depends(get_current_user_by_refresh_token)):
    return utils.auth.create_jwt_pair_by_user_id(current_user.id)
