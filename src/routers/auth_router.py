"""All auth methods and some useful stuff"""
from fastapi import APIRouter

import db
from db.models.user import UserSignin
from auth.utils import verify_password, create_token
from auth.token_schema import TokenSchema
from utils.utils import get_error_response, get_error_schema

router = APIRouter()


@router.post(
    "/signin",
    response_model=TokenSchema,
    responses={
        400: get_error_schema("Failed to signin")
    }
)
async def signin(user_data: UserSignin):
    """Auth user and generate JWT"""
    user = await db.user.get_by_name(user_data.name)

    if user is None:
        return get_error_response("Invalid login or password")

    if not verify_password(user_data.password, user.password_hash):
        return get_error_response("Invalid login or password")

    return {
        "access_token": create_token(user.name),
        "refresh_token": create_token(user.name, False),
    }
