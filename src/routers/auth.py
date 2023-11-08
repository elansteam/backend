from fastapi import APIRouter, HTTPException, Response, status, Depends
from pydantic import EmailStr
from starlette.responses import JSONResponse

from db.managers.user_database_manager import UserDatabaseManager
from db.models.user import User, UserSignup, UserSignin
from src.auth.utils import get_hashed_password, verify_password, create_token
from src.auth.TokenSchema import TokenSchema
from src.auth.utils import get_current_user

db = UserDatabaseManager()

router = APIRouter()


# TODO: Сделать метод только для админов, например напрямую передавать jwt токен
# TODO: Сделать адекватные коды возврата
@router.post(
    "/signup",
    response_model=User,
    responses={
        400: {
            "description": "Failed to create user",
            "content": {
                "application/json": {
                    "example": {"detail": [
                        {"msg": "User with this user name already exists"}
                    ]},
                }
            }
        }
    }
)
async def signup(user_auth: UserSignup, user: User = Depends(get_current_user)):
    """Создает нового пользователя в базе данных"""

    user_by_name = await db.get_by_name(user_auth.user_name)
    if user_by_name is not None:
        return JSONResponse(status_code=400, content={"detail": [
            {"msg": "User with this user name already exists"}
        ]})

    password_hash = get_hashed_password(user_auth.password)

    user_to_create = {
        **user_auth.model_dump(),
        "password_hash": password_hash
    }

    user = User.model_validate(user_to_create)

    await db.create(user)

    return user


@router.post(
    "/signin",
    response_model=TokenSchema,
    responses={
        400: {
            "description": "Invalid data for signin",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "msg": "Invalid user name or password"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def signin(user_data: UserSignin):
    user = await db.get_by_name(user_data.user_name)

    if user is None:
        return JSONResponse(status_code=400, content={
            "detail": [{
                "msg": "Invalid login or password"
            }]
        })

    if not verify_password(user_data.password, user.password_hash):
        return JSONResponse(status_code=400, content={
            "detail": [{
                "msg": "Invalid login or password"
            }]
        })

    return {
        "access_token": create_token(user.user_name, ),
        "refresh_token": create_token(user.user_name, False),
    }

