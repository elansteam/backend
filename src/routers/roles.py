"""Roles endpoints"""
from fastapi import APIRouter, Depends
from db.managers.role_database_manager import RoleDatabaseManager
from db.models.user import User
from db.models.role import Role
from auth.utils import auth_user, Permissions
from utils.utils import get_error_schema, get_error_response

router = APIRouter()

db = RoleDatabaseManager()


@router.post(
    "/create",
    response_model=Role,
    responses={
        400: get_error_schema("Failed to create role")
    }
)
async def create(role: Role,
                 _current_user: User = Depends(auth_user(
                     Permissions.C_CREATE_ROLE
                 ))):
    """Role creation"""

    if await db.get_by_name(role.name) is not None:
        return get_error_response(f"Role with name <{role.name}> are exist yet")

    await db.create(role)
    return role
