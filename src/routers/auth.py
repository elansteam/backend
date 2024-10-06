from fastapi import APIRouter, Depends
from fastapi import status as http_status

import utils.auth
from utils.auth import get_current_user_by_refresh_token
from utils.response import SuccessfulResponse, ErrorCodes, ErrorResponse
from db import methods
from typings import types, RQ, RS


router = APIRouter()


@router.post("/signin", response_model=SuccessfulResponse[RS.auth.signin])
async def signin(request: RQ.auth.signin):
    user: types.User | None = None
    if request.id:
        user = methods.get_user(request.id)
    elif request.email:
        user = methods.get_user_by_email(request.email)

    if user is None:
        raise ErrorResponse(
            code=ErrorCodes.NOT_FOUND, http_status_code=http_status.HTTP_404_NOT_FOUND, message="User not found"
        )

    if not utils.auth.verify_password(request.password, user.hashed_password):
        raise ErrorResponse(
            code=ErrorCodes.ACCESS_DENIED, http_status_code=http_status.HTTP_403_FORBIDDEN, message="Incorrect password"
        )

    return utils.auth.create_jwt_pair_by_user_id(user.id)


@router.get("/refresh", response_model=SuccessfulResponse[RS.auth.refresh])
async def refresh(current_user: types.User = Depends(get_current_user_by_refresh_token)):
    return utils.auth.create_jwt_pair_by_user_id(current_user.id)
