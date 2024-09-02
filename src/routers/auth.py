from fastapi import APIRouter, Depends
from fastapi import status as http_status

import utils.auth
from utils.auth import get_current_user_by_refresh_token
from utils.response import SuccessfulResponse, ErrorCodes, ErrorResponse
from db import methods
from db.types import types, RS, RQ


router = APIRouter()


@router.post("/signin", response_model=SuccessfulResponse[RS.auth.signin])
async def signin(request: RQ.auth.signin):
    user: types.User | None = None
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
async def refresh(current_user: types.User = Depends(get_current_user_by_refresh_token)):
    return utils.auth.create_jwt_pair_by_user_id(current_user.id)
