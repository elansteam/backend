from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.grole_database_manager import GRoleDatabaseManager
from db.managers.gpermission_database_manager import GPermissionDatabaseManager
from db.managers.group_database_manager import GroupDatabaseManager, Group
from src.auth.utils import get_current_user
from starlette.responses import JSONResponse
from src.auth.utils import get_current_user, AUTH_RESPONSE_MODEL, AUTH_FAILED
from src.db.models.grole import GRole
from db.models.user import User

router = APIRouter()

db_groles = GRoleDatabaseManager()
db_perms = GPermissionDatabaseManager()
db_groups = GroupDatabaseManager()


@router.post(
    "/create",
    response_model=GRole,
    responses={
        400: {
            "description": "Failed to create grole",
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
async def create(grole: GRole, current_user: User = Depends(get_current_user)):
    """Создание grole для группы"""

    if "admin" not in current_user.roles:
        return AUTH_FAILED

    if await db_groles.get_by_name(grole.name, grole.group) is not None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"GRole with name <{grole.name}> and group <{grole.group}> are exist yet"
                }]}
        )

    # TODO: do async for
    for perm_name in grole.gpermissions:
        if await db_perms.get_by_name(perm_name) is None:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": [{
                        "msg": f"GPermission with name <{perm_name}> isn`t exist"
                    }]}
            )

    group = await db_groups.get_by_name(grole.group)

    if group is None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"Group with name <{grole.group}> isn`t exist"
                }]}
        )

    await db_groles.create(grole)

    await db_groups.add_grole(grole.group, grole.name)
    return grole
