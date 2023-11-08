from fastapi import APIRouter, HTTPException, Response, status
from pydantic import EmailStr
from starlette.responses import JSONResponse

from db.managers.user_database_manager import UserDatabaseManager
from db.models.user import User, UserAuth
from src.auth.utils import get_hashed_password, verify_password

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
async def create_user(user_auth: UserAuth):
    """Создает нового пользователя в базе данных"""

    user_by_name = await db.get_by_user_name(user_auth.user_name)
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
