from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.grole_database_manager import GRoleDatabaseManager
from db.managers.gpermission_database_manager import GPermissionDatabaseManager
from db.managers.group_database_manager import GroupDatabaseManager, Group
from db.managers.user_database_manager import UserDatabaseManager
from src.auth.utils import get_current_user
from starlette.responses import JSONResponse
from src.auth.utils import get_current_user, AUTH_RESPONSE_MODEL, AUTH_FAILED
from src.db.models.grole import GRole
from db.models.user import User

router = APIRouter()

db_groles = GRoleDatabaseManager()
db_perms = GPermissionDatabaseManager()
db_groups = GroupDatabaseManager()
db_users = UserDatabaseManager()


@router.post(
    "/create",
    response_model=Group,
    responses={
        400: {
            "description": "Failed to create group",
            "content": {
                "application/json": {
                    "example": {"detail": [{
                        "msg": "error message",
                    }]},
                }
            }
        },
        401: AUTH_RESPONSE_MODEL
    }
)
async def create(group: Group, current_user: User = Depends(get_current_user)):
    """Создание группы"""

    if "admin" not in current_user.roles:
        return AUTH_FAILED

    # проверка на уникальность группы
    if await db_groups.get_by_name(group.name) is not None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"Group with name <{group.name}> are exist yet"
                }]}
        )

    # Проверка на существование владельца
    if await db_users.get_by_name(group.owner) is None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"Owner with name <{group.owner}> isn`t exist"
                }]}
        )

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

    group.members[group.owner] = "owner"

    await db_groups.create(group)
    return group
