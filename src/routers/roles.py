from fastapi import APIRouter, Depends
from db.managers.role_database_manager import RoleDatabaseManager
from db.managers.permission_database_manager import PermissionDatabaseManager
from auth.utils import auth_user
from utils.utils import get_error_schema, get_error_response
from db.models.role import Role
from db.models.user import User

router = APIRouter()

db = RoleDatabaseManager()
db_perms = PermissionDatabaseManager()


@router.post(
    "/create",
    response_model=Role,
    responses={
        400: get_error_schema("Failed to create role")
    }
)
async def create(role: Role, current_user: User = Depends(auth_user("admin"))):
    """Создание роли"""

    if await db.get_by_name(role.name) is not None:
        return get_error_response(f"Role with name <{role.name}> are exist yet")

    # TODO: do async for
    for perm_name in role.permissions:
        if await db_perms.get_by_name(perm_name) is None:
            return get_error_response(f"Permission with name <{perm_name}> isn`t exist")

    await db.create(role)
    return role
