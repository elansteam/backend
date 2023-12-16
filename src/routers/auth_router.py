"""All auth methods and some useful stuff"""
from fastapi import APIRouter

import db
from db.models.user import UserSignin
from auth.utils import verify_password, create_token
from auth.token_schema import TokenSchema
from utils.regex_validators import validate_email
from utils.response_utils import get_error_response, get_error_schema

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
    user_login = user_data.login
    if user_login.startswith("id") and user_login[2:].isdecimal(): # login by id (e.g. id1234567890)
        user = await db.user.get(int(user_login[2:]))
    if user is None and validate_email(user_login): # login by email
        user = await db.user.get_by_email(user_login)
    if user is None: # login by username
        entity = await db.domain.resolve(user_login)
        if entity is not None and entity.entity_type == "user":
            user = await db.user.get(entity.id)

    if user is None:
        return get_error_response("Invalid login")

    if not verify_password(user_data.password, user.password_hash):
        return get_error_response("Invalid password")

    return {
        "access_token": create_token(str(user.id)),
        "refresh_token": create_token(str(user.id), False),
    }
