"""Users endpoints"""
from fastapi import APIRouter, Depends

import db
from db.models.user import User, UserSignup
from db.models.role import Role
from auth.utils import auth_user, Permissions
from auth.utils import get_hashed_password
from utils.response_utils import get_error_response, get_error_schema

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
                     Permissions.CAN_CREATE_USER
                 ))):
    """Creating new user in database"""
    raise NotImplementedError()
    # entity = await db.domain.resolve(user_auth.name)
    # if user_by_name is not None:
    #     return get_error_response(
    #         f"User with this user name <{user_auth.name}> already exists")

    # password_hash = get_hashed_password(user_auth.password)

    # user_to_create = {
    #     **user_auth.model_dump(),
    #     "password_hash": password_hash
    # }

    # user_to_create.pop("password")

    # user = User(**user_to_create)

    # await db.user.create(user)

    # return user


@router.post(
    "/add_role",
    response_model=Role,
    responses={
        400: get_error_schema("Failed to add role to user")
    }
)
async def add_role_to_user(user_id: int, role_id: str,
                           _current_user: User = Depends(auth_user(
                               Permissions.CAN_ADD_ROLE_TO_USER
                           ))):
    """Adding role to user"""
    user_to_add = await db.user.get(user_id)

    if user_to_add is None:
        return get_error_response(f"User with id {user_id} doesn't exist")

    role = await db.role.get(role_id)

    if role is None:
        return get_error_response(f"Role with id <{role_id}> doesn't exist")

    if role_id in user_to_add.roles:
        return get_error_response(
            f"Role with id <{role_id}> already exists for user with id <{user_id}>"
        )

    await db.user.add_role(user_id, role_id)
    return role
