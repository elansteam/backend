"""Endpoints with group roles"""
from fastapi import APIRouter, Depends
import db
from db.models.user import User
from src.auth.utils import auth_user, Permissions
from src.db.models.group_role import GroupRole
from utils.utils import get_error_response, get_error_schema

router = APIRouter()


@router.post(
    "/create",
    response_model=GroupRole,
    responses={
        400: get_error_schema("Failed to create group roles"),
    }
)
async def create(group_role: GroupRole,
                 _current_user: User = Depends(auth_user(
                     Permissions.C_CREATE_GROUP_ROLE
                 ))):
    """Greate group role for group"""
    if await db.group_role.get_by_name(group_role.name, group_role.group) is not None:
        return get_error_response(
            f"Group role with name <{group_role.name}> and group with name <{group_role.group}> "
            f"doesn't exist")

    group = await db.group.get_by_name(group_role.group)

    if group is None:
        return get_error_response(f"Group with name <{group_role.group}> doesn't exist")

    await db.group_role.create(group_role)

    await db.group.add_group_role(group_role.group, group_role.name)
    return group_role
