from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.user_database_manager import UserDatabaseManager
from db.managers.role_database_manager import RoleDatabaseManager
from starlette.responses import JSONResponse
from src.auth.utils import get_current_user

from src.db.models.user import User
from db.models.role import Role

router = APIRouter()

db = UserDatabaseManager()
role_db = RoleDatabaseManager()


@router.get("/get_by_id/{oid}", response_model=User)
async def get_by_id(oid: str, user: User = Depends(get_current_user)):
    """Получение пользователя по ID"""
    user = await db.get_by_id(OID(oid))
    return user


@router.post(
    "/add_role",
    response_model=Role,
    responses={
        400: {
            "description": "Failed to add role to user",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "msg": "error message"
                        }]
                    }
                }
            }
        }
    }
)
async def add_role_to_user(user_name: str, role_name: str, user: User = Depends(get_current_user)):
    """Добавляет роль пользователю"""
    user = await db.get_by_name(user_name)

    if user is None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"User with user name {user_name} isn`t exist"
                }]
            }
        )

    role = await role_db.get_by_name(role_name)

    if role is None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"Role with name <{role_name}> isn`t exist"
                }]
            }
        )

    if role_name in user.roles:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"Role with name <{role_name}> are exist now in User <{user_name}>"
                }]
            }
        )

    await db.add_role(user_name, role_name)
    return role
