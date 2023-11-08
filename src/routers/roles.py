from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.role_database_manager import RoleDatabaseManager
from db.managers.permission_database_manager import PermissionDatabaseManager
from src.auth.utils import get_current_user
from starlette.responses import JSONResponse
from src.auth.utils import get_current_user
from src.db.models.role import Role
from db.models.user import User

router = APIRouter()

db = RoleDatabaseManager()
db_perms = PermissionDatabaseManager()


@router.post(
    "/create",
    response_model=Role,
    responses={
        400: {
            "description": "When permissions isn`t exists",
            "content": {
                "application/json": {
                    "example": {"detail": [{
                        "msg": "error message",
                    }]},
                }
            }
        }
    }
)
async def create(role: Role, user: User = Depends(get_current_user)):
    """Создание роли"""

    if await db.get_by_name(role.name) is not None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": [{
                    "msg": f"Role with name <{role.name}> are exist yet"
                }]}
        )

    # TODO: do async for
    for perm_name in role.permissions:
        if await db_perms.get_by_name(perm_name) is None:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": [{
                        "msg": f"Permission with name <{perm_name}> isn`t exist"
                    }]}
            )

    await db.create_role(role)

    return role
