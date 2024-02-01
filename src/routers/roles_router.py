"""Roles endpoints"""
from loguru import logger
from fastapi import APIRouter, Depends
from db.models.user import User
from db.models.role import Role, RoleCreate, role_name_to_id
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
async def create(role: RoleCreate,
                 _current_user: User = Depends(auth_user(
                     Permissions.CREATE_ROLE
                 ))):
    """
    Role creation
    Args:
        role: role to create
        _current_user: current user which created the role
    Returns:
        Created role
    """
    role_id = role_name_to_id(role.name)

    if await db.role.get(role_id) is not None:
        logger.info(f"Role with id <{role_id}> already exists")
        return get_error_response("ROLE_ALREADY_EXISTS")

    await db.role.insert(Role(
        _id=role_id,
        **(role.model_dump(by_alias=True))
    ))
    result_role = await db.role.get(role_id)

    return get_response(result_role)
