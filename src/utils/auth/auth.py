import datetime
from typing import Literal
import jose.jwt
from passlib.context import CryptContext
from fastapi import Header
from fastapi import status as http_status

from db import methods
from db.types import types
from utils import response
from config import config


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_auth_header_credentials(
    header: str,
    prefix: Literal["Bearer", "Service"]
) -> str:
    credentials = header.split()

    error_message = f"Incorrect authorization header format. Format: {prefix} <auth>"

    if len(credentials) != 2:
        raise response.ErrorResponse(
            code=response.ErrorCodes.TOKEN_VALIDATION_FAILED,
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
            message=error_message
        )

    current_prefix, token = credentials[0], credentials[1]

    if current_prefix != prefix:
        raise response.ErrorResponse(
            code=response.ErrorCodes.TOKEN_VALIDATION_FAILED,
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
            message=error_message
        )

    return token

def convert_role_code_to_permissions(role_code: int) -> list[int]:
    permissions = []
    i = 0
    while (1 << i) <= role_code:
        if (role_code >> i) & 1:
            permissions.append(i)
        i += 1
    return permissions

def convert_permissions_to_role_code(permissions: list[int]) -> int:
    role_code = 0
    for permission in permissions:
        role_code += 1 << permission
    return role_code

def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def create_jwt(
    subject: str,
    expiration_time_minutes: int,
    secret_key: str
) -> str:
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=expiration_time_minutes
    )

    data_to_encode = {
        "exp": expiration_time,
        "subject": subject
    }

    jwt = jose.jwt.encode(
        data_to_encode,
        secret_key
    )
    return jwt

def decode_jwt(
    jwt: str,
    secret_key: str
) -> dict[Literal["subject"], str]:
    """
    ### Raises:
        - `ValueError`: If there is no subject field in decoded jwt
        - `response.ErrorResponse`: *TOKEN_EXPIRED*
        - `response.ErrorResponse`: *TOKEN_VALIDATION_FAILED*
    """
    try:
        payload = jose.jwt.decode(
            jwt,
            secret_key
        )

        subject = payload.get("subject", None)
        if subject is None:
            raise ValueError("There is no <subject> field in jwt")

        return {
            "subject": subject
        }
    except jose.ExpiredSignatureError as exc:
        raise response.ErrorResponse(
            code=response.ErrorCodes.TOKEN_EXPIRED,
            message="Token signature expired",
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        ) from exc
    except Exception as exc:
        raise response.ErrorResponse(
            code=response.ErrorCodes.TOKEN_VALIDATION_FAILED,
            message="Token validation failed",
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        ) from exc

def create_jwt_pair_by_user_id(user_id: int) -> types.JWTPair:
    return types.JWTPair(
        access_token=create_jwt(
            str(user_id),
            expiration_time_minutes=config.auth.access_token_expire_minutes,
            secret_key=config.auth.jwt_access_secret_key.get_secret_value()
        ),
        refresh_token=create_jwt(
            str(user_id),
            expiration_time_minutes=config.auth.refresh_token_expire_minutes,
            secret_key=config.auth.jwt_refresh_secret_key.get_secret_value()
        )
    )

def get_current_user(authorization: str = Header()) -> types.User:
    token = get_auth_header_credentials(authorization, "Bearer")

    subject = decode_jwt(token, config.auth.jwt_access_secret_key.get_secret_value())["subject"]

    if subject.isnumeric() and (user := methods.helpers.get_object_by_id(int(subject), types.User)) is not None:
        return user

    raise response.ErrorResponse(
        code=response.ErrorCodes.ACCESS_DENIED,
        http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        message="Could not found user by token"
    )

def get_current_user_by_refresh_token(authorization: str = Header()) -> types.User:
    token = get_auth_header_credentials(authorization, "Bearer")

    subject = decode_jwt(token, config.auth.jwt_refresh_secret_key.get_secret_value())["subject"]

    if subject.isnumeric() and (user := methods.helpers.get_object_by_id(int(subject), types.User)) is not None:
        return user

    raise response.ErrorResponse(
        code=response.ErrorCodes.ACCESS_DENIED,
        http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        message="Could not found user by token"
    )

def service_auth(authorization: str = Header()) -> None:
    if get_auth_header_credentials(authorization, "Service") != config.auth.service_token.get_secret_value():
        raise response.ErrorResponse(
            code=response.ErrorCodes.ACCESS_DENIED,
            http_status_code=http_status.HTTP_401_UNAUTHORIZED
        )
