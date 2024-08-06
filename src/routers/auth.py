from fastapi import APIRouter

import utils.auth
from utils.response import SuccessfulResponse, ErrorCodes, ErrorResponse
from db import methods
from db import types


router = APIRouter()


@router.post("/signup", response_model=SuccessfulResponse[types.auth.JWTPair])
async def signup(
    user_signup: types.user.UserSignup
):
    if user_signup.domain is not None:
        if not methods.domains.reserve_entity(user_signup.domain):
            raise ErrorResponse(
                code=ErrorCodes.NAME_ALREADY_TAKEN,
                message="Domain already taken"
            )

    password_hash = utils.auth.hash_password(user_signup.password)

    inserted_user_id = methods.users.insert_user_document_with_id({
        "email": user_signup.email,
        "domain": user_signup.domain,
        "hashed_password": password_hash
    })

    if inserted_user_id is None:
        raise ErrorResponse(
            code=ErrorCodes.NAME_ALREADY_TAKEN,
            message="There is user with identical email"
        )

    if user_signup.domain is not None:
        methods.domains.attach_to_entity(
            user_signup.domain,
            inserted_user_id,
            "user"
        )

    return utils.auth.create_jwt_pair_by_user_id(inserted_user_id)

@router.post("/signin", response_model=SuccessfulResponse[types.auth.JWTPair])
async def signin(
    siginin_input: types.auth.SignInInput
):
    user: types.user.User | None = None
    if siginin_input.id:
        user = methods.users.get(siginin_input.id)
    elif siginin_input.domain:
        user_id = methods.domains.resolve_id(siginin_input.domain, "user")
        if user_id:
            user = methods.users.get(user_id)
    elif siginin_input.email:
        user = methods.users.get_by_email(siginin_input.email)

    if user is None:
        raise ErrorResponse(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            http_status_code=404,
            message="User not found"
        )

    if not utils.auth.verify_password(siginin_input.password, user.hashed_password):
        raise ErrorResponse(
            code=ErrorCodes.ACCESS_DENIED,
            http_status_code=403,
            message="Incorrect password"
        )

    return utils.auth.create_jwt_pair_by_user_id(user.id)
