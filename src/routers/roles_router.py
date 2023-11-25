"""Roles endpoints"""
from fastapi import APIRouter, Depends
from db.models.user import User
from db.models.role import Role
from auth.utils import auth_user, Permissions
from utils.utils import get_error_schema, get_error_response
import db

router = APIRouter()


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

    if await db.role.get_by_name(role.name) is not None:
        return get_error_response(f"Role with name <{role.name}> are exist yet")

    await db.role.create(role)
    return role
