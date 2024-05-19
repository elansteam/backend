"""
Helpers for auth stuff
"""

from loguru import logger
from passlib.context import CryptContext
from starlette import status as http_status
from fastapi import Header
import datetime
import jose

from db import methods
from db.models.user import User
from db.annotations import RoleCodeAnnotation

from auth.permissions import Permissions
from utils import response_utils
from config import config


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def has_role_permissions(
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

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(
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

    user = methods.users.get(int(token_sub))

    if user is None:
        raise response_utils.ResponseWithErrorCode(
            code=response_utils.ResponseErrorCodes.COULD_NOT_FIND_USER_BY_TOKEN,
            message="Could not find user by this token",
            http_status_code=http_status.HTTP_401_UNAUTHORIZED,
        )

    return user


def auth_user(*permissions: Permissions):
    """
    Dependency, that authorize user with given permissions by jwt token in 
    Authorization header.
    
    Usage example:
    >>> def endpoint(user: User = Depends(auth_user(Permissions.CREATE_ROLE)))
    Args:
        *permissions: Permissions, which must contain user roles
    Returns:
        Function that auth user by given permissions and auth header
    """

    def wrapper(authorization: str = Header()) -> User:
        """
        Authorization user by given permissions and auth header.
        Args:
            authorization: Authorization header in format: Bearer <auth_token>
        Returns:
            Authorized user object
        Raises:
            ResponseWithErrorCode: validation error or access denied
        """
        # validate authorization header
        credentials = authorization.split()
        if len(credentials) != 2:
            raise response_utils.ResponseWithErrorCode(
                code=response_utils.ResponseErrorCodes.INCORRECT_AUTH_HEADER_FOMAT,
                http_status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Incorrect authorization header format. Format: Bearer <auth>"
            )

        bearer, token, *_ = *credentials, None

        if bearer != "Bearer" or token is None:
            raise response_utils.ResponseWithErrorCode(
                code=response_utils.ResponseErrorCodes.INCORRECT_AUTH_HEADER_FOMAT,
                http_status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Incorrect authorization header format. Format: Bearer <auth>"
            )

        user = get_user_by_access_jwt(token)

        permissions_mask = 0

        for role_name in user.roles:
            role = methods.roles.get(role_name)
            if role is None:
                logger.error(f"Role with name <{role_name}> not found")
                continue
            permissions_mask |= role.role_code

        if not has_role_permissions(
            permissions_mask,
            *permissions
        ):
            required_permissions = []

            for permission in permissions:
                if not has_role_permissions(permissions_mask, permission):
                    required_permissions.append(permission.name)

            raise response_utils.ResponseWithErrorCode(
                code=response_utils.ResponseErrorCodes.ACCESS_DENIED,
                http_status_code=http_status.HTTP_403_FORBIDDEN,
                message=f"Missing permissions: {' '.join(required_permissions)}"
            )
        
        return user

    return wrapper
