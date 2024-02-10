"""All auth methods and some useful stuff"""
from typing import Literal


import db
from db.models.user import UserSignup, User
from auth.utils import get_hashed_password
from auth.utils import verify_password, create_token, auth_user
from auth.token_schema import TokenSchema
from utils.response_utils import get_error_response, get_response_model, get_error_schema, \
    get_response
from fastapi import APIRouter, Depends
from db.models.annotations import RoleCodeAnnotation

router = APIRouter()


@router.get(
    "/signin",
    response_model=get_response_model(TokenSchema),
    responses={
        400: get_error_schema("Failed to signin with provided credentials.")
    }
)
async def signin(login: str, password: str, login_type: Literal["email", "domain", "id"]):
    """Auth user and generate JWT"""
    user = None
    match login_type:
        case "email":
            user = await db.user.get_by_email(login)
        case "domain":
            entity = await db.domain.resolve(login)
            if entity is not None and entity.entity_type == "user" and entity.entity_id is not None:
                user = await db.user.get(entity.entity_id)
        case "id":
            user = await db.user.get(int(login))
    if user is None:
        return get_error_response("INVALID_LOGIN")

    if not verify_password(password, user.password_hash):
        return get_error_response("INVALID_PASSWORD")

    return get_response({
        "access_token": create_token(str(user.id)),
        "refresh_token": create_token(str(user.id), False),
    })


@router.post(
    "/signup",
    response_model=get_response_model(User),
    responses={
        400: get_error_schema("Signup failed")
    }
)
async def signup(user: UserSignup):
    """Creating new user"""

    password_hash = get_hashed_password(user.password)

    user_to_create = {
        **user.model_dump(),
        "password_hash": password_hash,
        "_id": 1  # not used
    }

    user_with_exact_email = await db.user.get_by_email(user.email)
    if user_with_exact_email is not None:
        return get_error_response("EMAIL_IN_USE")

    if user.domain is not None:
        status = await db.domain.reserve(user.domain)
        if status is False:
            return get_error_response("DOMAIN_IN_USE")

    try:
        created_user_id = await db.user.insert_with_id(
            User(**user_to_create)
        )
    except Exception as e:
        if user.domain is not None:
            await db.domain.delete(user.domain)  # deleting reserved entity
        raise e

    if user.domain is not None:
        await db.domain.attach(user.domain, "user", created_user_id)

    created_user = await db.user.get(created_user_id)
    return get_response(created_user)


@router.get(
    "/refresh",
    response_model=get_response_model(TokenSchema),
    responses={
        400: get_error_schema("Failed to refresh")
    }
)
async def refresh_token(_current_user: User = Depends(auth_user())):
    """Refresh tokens"""

    return get_response({
        "access_token": create_token(str(_current_user.id)),
        "refresh_token": create_token(str(_current_user.id), False),
    })

@router.get(
    "/user_permissions",
    responses={
        400: get_error_schema("Failed to get user permissions")
    }
)
async def user_permissions(_current_user: User = Depends(auth_user())) -> RoleCodeAnnotation:
    """Get user permissions"""

    result_mask = 0

    for role_name in _current_user.roles:
        cur_role = await db.role.get(role_name)
        if cur_role is not None:
            result_mask |= cur_role.role_code
    return result_mask

