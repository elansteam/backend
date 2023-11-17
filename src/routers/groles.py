from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.grole_database_manager import GRoleDatabaseManager
from db.managers.gpermission_database_manager import GPermissionDatabaseManager
from db.managers.group_database_manager import GroupDatabaseManager, Group
from src.auth.utils import get_current_user, auth_user
from starlette.responses import JSONResponse
from src.auth.utils import get_current_user, AUTH_RESPONSE_MODEL, AUTH_FAILED
from src.db.models.grole import GRole
from db.models.user import User
from utils.utils import get_error_response, get_error_schema

router = APIRouter()

db_groles = GRoleDatabaseManager()
db_perms = GPermissionDatabaseManager()
db_groups = GroupDatabaseManager()


@router.post(
    "/create",
    response_model=GRole,
    responses={
        400: get_error_schema("Failed to create grole"),
    }
)
async def create(grole: GRole, current_user: User = Depends(auth_user("admin"))):
    """Создание grole для группы"""

    if await db_groles.get_by_name(grole.name, grole.group) is not None:
        return get_error_response(
            f"GRole with name <{grole.name}> and group <{grole.group}> are exist yet")

    # TODO: do async for
    for perm_name in grole.gpermissions:
        if await db_perms.get_by_name(perm_name) is None:
            return get_error_response(f"GPermission with name <{perm_name}> isn`t exist")

    group = await db_groups.get_by_name(grole.group)

    if group is None:
        return get_error_response(f"Group with name <{grole.group}> isn`t exist")

    await db_groles.create(grole)

    await db_groups.add_grole(grole.group, grole.name)
    return grole
