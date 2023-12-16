"""Endpoints with group roles"""
from fastapi import APIRouter, Depends
import db
from db.models.user import User
from db.models.group_role import GroupRole
from auth.utils import auth_user, Permissions
from utils.response_utils import get_error_response, get_error_schema

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
                     Permissions.CAN_CREATE_GROUP_ROLE
                 ))):
    """Greate group role for group"""
    group = await db.group.get(group_role.group)

    if group is None:
        return get_error_response(f"Group with id <{group_role.group}> doesn't exist")

    if await db.group_role.get(
        group_role.group, f"group{group_role.group}_{group_role.id}"
    ) is not None:
        return get_error_response(
            f"Group role with given id <{group_role.id}> already exists"
        )
    # group from basemodel has id=<role_id>
    # so we should change it to the DB format - group<group_id>_<role_id>
    new_group_role = GroupRole(
        _id=f"group{group_role.group}_{group_role.id}",
        name=group_role.name, group=group_role.group,
        role_code=group_role.role_code,
        description=group_role.description
    )
    await db.group_role.create(new_group_role)
    await db.group.add_role(group_role)
    return group_role
