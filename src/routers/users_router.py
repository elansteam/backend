"""Users endpoints"""
from typing import List, Any

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from db.models.user import User
import db
from utils.response_utils import get_error_response, get_response_model, get_error_schema, \
    get_response
from auth.utils import auth_user
from auth.utils import Permissions
from db.models.annotations import IntIdAnnotation

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


@router.get(
    "/get_current",
    response_model=get_response_model(User),
    responses={
        400: get_error_schema("Failed to retrieve current user")
    }
)
async def get_current_user(_current_user: User = Depends(auth_user())):
    """Get current user"""
    return get_response(_current_user)


@router.get(
    "/get_groups",
    responses={
        400: get_error_schema("Failed to retrieve groups")
    }
)
async def get_groups(
        _id: IntIdAnnotation,
        _current_user: User = Depends(auth_user())
) -> Any | IntIdAnnotation:
    """Retrieve all groups thet has user"""

    user = await db.user.get(_id)

    if user is None:
        return get_error_response("USER_NOT_FOUND")

    groups = await db.group.get_all()

    result = []

    for group in groups:
        if group.owner == _id:
            result.append(group.id)
            continue
        for member in group.members:
            if member.id == _id:
                result.append(group.id)
                break

    return get_response({"result": result})
