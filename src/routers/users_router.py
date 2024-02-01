"""Users endpoints"""
from fastapi import APIRouter, Depends

from db.models.user import User
import db
from utils.response_utils import get_error_response, get_response_model, get_error_schema, \
    get_response
from auth.utils import auth_user
from auth.utils import Permissions

router = APIRouter()


@router.post(
    "/add_role",
    response_model=get_response_model(),
    responses={
        400: get_error_schema("Failed to add role")
    }
)
async def add_role(user_id: int, role_id: str,
                   _current_user: User = Depends(auth_user(
                       Permissions.CHANGE_USER_ROLES
                   ))):
    """Add a role to the user"""
    user_to_add = await db.user.get(user_id)

    if user_to_add is None:
        return get_error_response("USER_NOT_FOUND")

    role_to_add = await db.role.get(role_id)

    if role_to_add is None:
        return get_error_response("ROLE_NOT_FOUND")

    if role_id in user_to_add.roles:
        return get_error_response("ROLE_ALREADY_EXISTS")

    await db.user.add_role(user_id, role_id)

    return get_response()


@router.post(
    "/delete_role",
    response_model=get_response_model(),
    responses={
        400: get_error_schema("Failed to delete role from user")
    }
)
async def delete_role(user_id: int, role_id: str,
                      _current_user: User = Depends(auth_user(
                          Permissions.CHANGE_USER_ROLES
                      ))):
    """Delete a role from the user"""

    user_to_delete = await db.user.get(user_id)

    if user_to_delete is None:
        return get_error_response("USER_NOT_FOUND")

    role_to_delete = await db.role.get(role_id)

    if role_to_delete is None:
        return get_error_response("ROLE_NOT_FOUND")

    if role_id not in user_to_delete.roles:
        return get_error_response("ROLE_NOT_EXISTS")

    await db.user.delete_role(user_id, role_id)

    return get_response()
