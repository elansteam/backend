from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.user_database_manager import UserDatabaseManager
from db.managers.role_database_manager import RoleDatabaseManager
from starlette.responses import JSONResponse
from auth.utils import auth_user, Permissions
from utils.utils import get_error_response, get_error_schema

from db.models.user import User
from db.models.role import Role

router = APIRouter()

db = UserDatabaseManager()
role_db = RoleDatabaseManager()


# TODO: подумать, нужна ли эта хрень
# @router.get("/get_by_id/{oid}", response_model=User)
# async def get_by_id(oid: str, user: User = Depends(get_current_user)):
#     """Получение пользователя по ID"""
#     user = await db.get_by_id(OID(oid))
#     return user


@router.post(
    "/add_role",
    response_model=Role,
    responses={
        400: get_error_schema("Failed to add role to user")
    }
)
async def add_role_to_user(user_name: str, role_name: str,
                           current_user: User = Depends(auth_user(
                               Permissions.C_ADD_ROLE_TO_USER
                           ))):
    """Добавляет роль пользователю"""

    cur_user = await db.get_by_name(user_name)

    if cur_user is None:
        return get_error_response(f"User with user name {user_name} isn`t exist")

    role = await role_db.get_by_name(role_name)

    if role is None:
        return get_error_response(f"Role with name <{role_name}> isn`t exist")

    if role_name in cur_user.roles:
        return get_error_response(
            f"Role with name <{role_name}> are exist now in User <{user_name}>"
        )

    await db.add_role(user_name, role_name)
    return role
