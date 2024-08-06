import datetime
from typing import Literal
import jose.jwt
from passlib.context import CryptContext
from fastapi import Header
from starlette import status as http_status

from db import methods
from db.types.auth import JWTPair
from db.types.user import User
from db.types.common import IntegerId, RoleCode
from utils import response
from config import config
from .permissions import Permissions


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_auth_header_credentials(
    header: str,
    prefix: Literal["Bearer", "Service"]
) -> str:
    credentials = header.split()

    error_message = f"Incorrect authorization header format. Format: {prefix} <auth>"

    if len(credentials) != 2:
        raise response.ErrorResponse(
            code=response.ErrorCodes.INCORRECT_AUTH_HEADER_FOMAT,
            http_status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=error_message
        )

    current_prefix, token = credentials[0], credentials[1]

    if current_prefix != prefix:
        raise response.ErrorResponse(
            code=response.ErrorCodes.INCORRECT_AUTH_HEADER_FOMAT,
            http_status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=error_message
        )

    return token

def convert_role_code_to_permissions(role_code: RoleCode) -> list[int]:
    permissions = []
    i = 0
    while 1 << i <= role_code:
        if role_code >> i & 1 == 1:
            permissions.append(i)
        i += 1
    return permissions

def convert_permissions_to_role_code(permissions: list[int]) -> RoleCode:
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
            secret_key,
            # ! algorithms=["HS256"]
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

def create_jwt_pair_by_user_id(user_id: IntegerId) -> JWTPair:
    return JWTPair(
        access=create_jwt(
            str(user_id),
            expiration_time_minutes=config.auth.access_token_expire_minutes,
            secret_key=config.auth.jwt_access_secret_key.get_secret_value()
        ),
        refresh=create_jwt(
            str(user_id),
            expiration_time_minutes=config.auth.refresh_token_expire_minutes,
            secret_key=config.auth.jwt_refresh_secret_key.get_secret_value()
        )
    )

def auth_user(*permissions: Permissions):
    """
    Dependency, that authorize user with given permissions by **access** jwt token in
    Authorization header.

    Usage example:
    >>> def endpoint(user: User = Depends(auth_user(Permissions.CREATE_ROLE)))
    Args:
        permissions: Permissions, which must contain user roles
    Returns:
        Function that auth user by given permissions and auth header
    """

    def wrapper(authorization: str = Header()) -> User:
        token = get_auth_header_credentials(authorization, "Bearer")

        subject = decode_jwt(token, config.auth.jwt_access_secret_key.get_secret_value())["subject"]

        if subject.isnumeric():
            user_id = int(subject)

            user = methods.users.get(user_id)

            if user is not None:
                general_role_code = 0
                for role_name in user.roles:
                    role = methods.roles.get(role_name)
                    if role is None:
                        continue
                    general_role_code |= role.code

                user_permissions = convert_role_code_to_permissions(general_role_code)

                for permission in permissions:
                    if permission.value not in user_permissions:
                        raise response.ErrorResponse(
                            code=response.ErrorCodes.ACCESS_DENIED,
                            http_status_code=http_status.HTTP_403_FORBIDDEN
                        )
                return user

        raise response.ErrorResponse(
            code=response.ErrorCodes.ENTITY_NOT_FOUND,
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
            message="Could not found user by token"
        )
    return wrapper
