"""Roles endpoints"""
from fastapi import APIRouter, Depends
from db.models.user import User
from db.models.role import Role
from auth.utils import auth_user, Permissions
from utils.response_utils import get_error_schema, get_error_response, get_response, \
    get_response_model
import db

router = APIRouter()


@router.post(
    "/create",
    response_model=get_response_model(Role),
    responses={
        400: get_error_schema("Failed to create role")
    }
)
async def create(role: Role,
                 _current_user: User = Depends(auth_user(
                     Permissions.CREATE_ROLE
                 ))):
    """
    Role creation
    Args:
        role:
        _current_user:

    Returns:
        Created role
    """

    if await db.role.get(role.id) is not None:
        return get_error_response(f"Role with id <{role.id}> already exists")
    await db.role.insert(role)
    return get_response(role)
