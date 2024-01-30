"""
Helpers for auth stuff
"""
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from jose import jwt
from starlette import status
from starlette.responses import JSONResponse
from config import Config
import db
from db.models.user import User
from auth.Permissions import Permissions

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def has_role_permissions(role_staff: int, *permissions: Permissions) -> bool:
    """Check what role contains permissions
    Args:
        role_staff: representation permissions through converted to bits int32 number

    Returns:
        True - if role has permission, else False
    """
    for perm in permissions:
        if (role_staff >> perm.value) % 2 == 0:
            return False

    return True


def gen_code_staff_by_permissions(*permissions: Permissions) -> int:
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


AUTH_RESPONSE_MODEL = {
    "description": "Failed auth",
    "content": {
        "application/json": {
            "example": {"detail": [{"msg": "Auth failed"}]},
        }
    },
}

AUTH_FAILED = JSONResponse(
    status_code=401, content={"detail": [{"msg": "Auth failed"}]}
)


def get_hashed_password(password: str) -> str:
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


def create_token(
        subject: str, is_access=True, expires_delta: int | None = None
) -> str:
    """
    Generating JWT by data and expires time
    Args:
        subject: some useful data to code, like username
        is_access: if False generate refresh token with longer expiration time
        expires_delta: how long token available
    Returns:
        JWT in string
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    elif is_access:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=Config.Auth.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=Config.Auth.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Config.Auth.JWT_SECRET_KEY, Config.Auth.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str) -> User:
    """Get current user by access token or raise HTTPException
    Args:
        token (str): access token

    Raises:
        HTTPException: Raise 401/403 error if access token is invalid
    Returns:
        User: user object
    """
    try:
        payload = jwt.decode(token, Config.Auth.JWT_SECRET_KEY, algorithms=[Config.Auth.ALGORITHM])
        token_exp = payload["exp"]
        token_sub = payload["sub"]

        if datetime.fromtimestamp(token_exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = await db.user.get(int(token_sub))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find user",
        )

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
        HTTPException: Raise 403 error user hasn`t permissions
    """

    async def wrapper(user: User = Depends(get_current_user)) -> User:
        result_mask = 0

        for role_name in user.roles:
            cur_role = await db.role.get(role_name)
            if cur_role is not None:
                result_mask |= cur_role.permissions

        if not has_role_permissions(result_mask, *permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User <{user.name}> has no required permission"
            )
        return user

    return wrapper
