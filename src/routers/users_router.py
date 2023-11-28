"""Users endpoints"""
from fastapi import APIRouter, Depends

import db
from db.models.user import User, UserSignup
from db.models.role import Role
from auth.utils import auth_user, Permissions
from auth.utils import get_hashed_password
from utils.utils import get_error_response, get_error_schema

router = APIRouter()


@router.post(
    "/create",
    response_model=User,
    responses={
        400: get_error_schema("Failed to create user")
    }
)
async def create(user_auth: UserSignup,
                 _current_user: User = Depends(auth_user(
                     Permissions.C_CREATE_USER
                 ))):
    """Creating new user in database"""
    user_by_name = await db.user.get_by_name(user_auth.name)
    if user_by_name is not None:
        return get_error_response(
            f"User with this user name <{user_auth.name}> already exists")

    password_hash = get_hashed_password(user_auth.password)

    user_to_create = {
        **user_auth.model_dump(),
        "password_hash": password_hash
    }

    user_to_create.pop("password")

    user = User(**user_to_create)

    await db.user.create(user)

    return user


@router.post(
    "/add_role",
    response_model=Role,
    responses={
        400: get_error_schema("Failed to add role to user")
    }
)
async def add_role_to_user(user_name: str, role_name: str,
                           _current_user: User = Depends(auth_user(
                               Permissions.C_ADD_ROLE_TO_USER
                           ))):
    """Adding role to user"""

    cur_user = await db.user.get_by_name(user_name)

    if cur_user is None:
        return get_error_response(f"User with user name {user_name} doesn't exist")

    role = await db.role.get_by_name(role_name)

    if role is None:
        return get_error_response(f"Role with name <{role_name}> doesn't exist")

    if role_name in cur_user.roles:
        return get_error_response(
            f"Role with name <{role_name}> are exist now in User <{user_name}>"
        )

    await db.role.add_role(user_name, role_name)
    return role
