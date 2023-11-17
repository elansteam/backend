from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.grole_database_manager import GRoleDatabaseManager
from db.managers.gpermission_database_manager import GPermissionDatabaseManager
from db.managers.group_database_manager import GroupDatabaseManager, Group
from db.managers.user_database_manager import UserDatabaseManager
from src.auth.utils import get_current_user, auth_user
from starlette.responses import JSONResponse
from src.auth.utils import get_current_user, AUTH_RESPONSE_MODEL, AUTH_FAILED
from src.db.models.grole import GRole
from db.models.user import User
from utils.utils import get_error_response, get_error_schema
from config import Config

router = APIRouter()

db_groles = GRoleDatabaseManager()
db_perms = GPermissionDatabaseManager()
db_groups = GroupDatabaseManager()
db_users = UserDatabaseManager()


# TODO: add auth
@router.post(
    "/create",
    response_model=Group,
    responses={
        400: get_error_schema("Failed to create group"),
    }
)
async def create(group: Group, current_user: User = Depends(auth_user("admin"))):
    """Создание группы"""

    # проверка на уникальность группы
    if await db_groups.get_by_name(group.name) is not None:
        return get_error_response(f"Group with name <{group.name}> are exist yet",
                                  400)

    # Проверка на существование владельца
    if await db_users.get_by_name(group.owner) is None:
        return get_error_response(f"Owner with name <{group.owner}> isn`t exist",
                                  400)

    # Создание встроенных ролей
    # TODO вынести это в отдельное поле и сделать расширяемым
    await db_groles.create(GRole.model_validate(
        {
            "name": "owner",
            "group": group.name,
            "gpermissions": ["owner"],
            "description": "The most powerful role in group"
        }
    ))

    await db_groles.create(GRole.model_validate(
        {
            "name": "admin",
            "group": group.name,
            "gpermissions": ["admin"],
            "description": "Like owner but lower"  # FIXME
        }
    ))

    group.groles = []
    group.members = {}

    group.groles.append("owner")
    group.groles.append("admin")

    group.members[group.owner] = ["owner"]

    await db_groups.create(group)
    return group


# TODO: add auth
@router.post(
    "/add_user",
    response_model=User,
    responses={
        400: get_error_schema("Failed add user to group"),
        401: AUTH_RESPONSE_MODEL
    }
)
async def add_user(user_name: str, group_name: str, current_user: User = Depends(get_current_user)):
    if current_user is None:
        return AUTH_FAILED

    group = await db_groups.get_by_name(group_name)

    # Проверка на существование группы
    if group is None:
        return get_error_response(f"Group with name <{group_name}> isn`t exist")

    # аутентификация
    group_members = await db_groups.get_members(group_name)

    if current_user.name not in group_members:
        return AUTH_FAILED

    # TODO: добавить адекватную проверку на права пока КОСТЫЛЬ

    if group.owner != current_user.name:
        return AUTH_FAILED

    # проверка валидности данных
    user = await db_users.get_by_name(user_name)

    if user is None:
        return get_error_response(f"User with name <{user_name}> isn`t exist")

    await db_groups.add_user(group_name, user_name)

    return await db_users.get_by_name(user_name)
