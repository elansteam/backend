"""
Helpers for auth stuff
"""

from datetime import datetime
from passlib.context import CryptContext
from starlette import status as http_status
import jose

from db import methods
from db.models.user import User
from db.annotations import RoleCodeAnnotation

from auth.permissions import Permissions
from utils import response_utils
from config import config


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_role_code_for_permissions(
    role_code: RoleCodeAnnotation,
    *permissions: Permissions
) -> bool:
    """Checking if this role has permissions
    Args:
        role_code: representation permissions through converted to bits int32 number

    Returns:
        True - if role has permission, else False
    """
    for perm in permissions:
        if (role_code >> perm.value) % 2 == 0:
            return False
    return True


def generate_role_code(*permissions: Permissions) -> RoleCodeAnnotation:
    """
    Generate role code by permissions
    Args:
        *permissions: permissions, which should be contained in role code
    Returns:
        role code
    """
    role_code = 0
    for perm in permissions:
        role_code += 1 << perm.value

    return role_code


def hash_password(password: str) -> str:
    """
    Hashing password
    Args:
        password: password to hash

    Returns:
        hashed password
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Checks what hashed password is password
    Args:
        password: password
        hashed_password: password hash

    Returns:
        True if hash(password) equal to hashed_password, else False
    """
    return password_context.verify(password, hashed_password)


def create_jwt(
        subject: str,
        expiration_time_minutes: int
) -> str:
    """Create a JWT from a subject with expiration time in minutes

    Args:
        subject: Data to encode
        expiration_time_minutes: Token expiration time

    Returns:
        JWT as string
    """

    expiration_time = datetime.utcnow() + datetime.timedelta(
        minutes=expiration_time_minutes
    )

    to_encode = {  # it is neccessary to name field like "exp" and "sub"
        "exp": expiration_time,
        "sub": subject
    }

    created_jwt = jose.jwt.encode(
        to_encode,
        config.auth.jwt_access_secret_key.get_secret_value(),
        algorithm=config.auth.algorithm
    )
    return created_jwt


def get_user_by_access_jwt(jwt: str) -> User:
    """Get current user by access token or raise ResponseWithErrorCode
    Args:
        jwt: access token
    Raises:
        ResponseWithErrorCode: Raise 401 error if access token is invalid
    Returns:
        User: user object
    """
    try:
        payload = jose.jwt.decode(
            jwt,
            config.auth.jwt_access_secret_key.get_secret_value(),
            algorithms=[config.auth.algorithm]
        )
        token_sub = payload["sub"]

    except jose.ExpiredSignatureError as exc:
        raise response_utils.ResponseWithErrorCode(
            code=response_utils.ResponseErrorCodes.TOKEN_EXPIRED,
            message="Token signature expired",
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        ) from exc
    except Exception as exc:
        raise response_utils.ResponseWithErrorCode(
            code=response_utils.ResponseErrorCodes.TOKEN_VALIDATION_FAILED,
            message="Token validation failed",
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        ) from exc

    user = methods.user.get(int(token_sub))

    if user is None:
        raise response_utils.ResponseWithErrorCode(
            code=response_utils.ResponseErrorCodes.COULD_NOT_FIND_USER_BY_TOKEN,
            message="Could not find user by this token",
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        ) from exc

    return user


def auth_user(*permissions: Permissions):
    """
    Decorator
    Use:
    >>> def endpoint(user: User = Depends(auth_user(Permissions.CREATE_ROLE)))
    Auth user by permissions.
    Args:
        *permissions: Permissions, which must contain user roles
    Returns:
        function, which auth user
    Raises:
        AuthException: Raise 403 error user hasn`t permissions
    """
    ...
