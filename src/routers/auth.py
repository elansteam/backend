from fastapi import APIRouter, HTTPException, Response, status, Depends
from pydantic import EmailStr
from starlette.responses import JSONResponse

from db.managers.user_database_manager import UserDatabaseManager
from db.models.user import User, UserSignup, UserSignin
from src.auth.utils import get_hashed_password, verify_password, create_token
from src.auth.TokenSchema import TokenSchema
from src.auth.utils import get_current_user, auth_user
from utils.utils import get_error_response, get_error_schema

db = UserDatabaseManager()

router = APIRouter()


# TODO: Сделать метод только для админов, например напрямую передавать jwt токен
# TODO: Сделать адекватные коды возврата
@router.post(
    "/signup",
    response_model=User,
    responses={
        400: get_error_schema("Failed to create user")
    }
)
async def signup(user_auth: UserSignup):
    """Создает нового пользователя в базе данных"""

    user_by_name = await db.get_by_name(user_auth.name)
    if user_by_name is not None:
        return get_error_response(
            f"User with this user name <{user_auth.name}> already exists")

    password_hash = get_hashed_password(user_auth.password)

    user_to_create = {
        **user_auth.model_dump(),
        "password_hash": password_hash
    }

    user = User(**user_to_create)

    await db.create(user)

    return user


@router.post(
    "/signin",
    response_model=TokenSchema,
    responses={
        400: get_error_schema("Failed to signin")
    }
)
async def signin(user_data: UserSignin):
    """Авторизует пользователя и генерирует JWT"""
    user = await db.get_by_name(user_data.name)

    if user is None:
        return get_error_response("Invalid login or password")

    if not verify_password(user_data.password, user.password_hash):
        return get_error_response("Invalid login or password")

    return {
        "access_token": create_token(user.name),
        "refresh_token": create_token(user.name, False),
    }
