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
        400: get_error_schema("Failed to create grole"),
    }
)
async def create(grole: GroupRole,
                 _current_user: User = Depends(auth_user(
                     Permissions.C_CREATE_GROLE
                 ))):
    """Greate group role for group"""
    if await db.group_role.get_by_name(grole.name, grole.group) is not None:
        return get_error_response(
            f"GRole with name <{grole.name}> and group <{grole.group}> are exist yet")

    group = await db.group.get_by_name(grole.group)

    if group is None:
        return get_error_response(f"Group with name <{grole.group}> isn`t exist")

    await db.group_role.create(grole)

    await db.group.add_grole(grole.group, grole.name)
    return grole
