"""
Helpers for auth stuff
"""
from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from starlette import status
from db.managers.user_database_manager import UserDatabaseManager
from db.managers.role_database_manager import RoleDatabaseManager
from db.models.user import User
from starlette.responses import JSONResponse
from fastapi import Depends
from enum import Enum

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

# TODO: set to config
JWT_SECRET_KEY = "jwt_secret_key"  # should be kept secret
JWT_REFRESH_SECRET_KEY = "jwt_refresh_secret_key"  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Permissions(Enum):
    """Перечисление всех прав"""
    ADMIN = 0
    C_SIGNUP = 1
    C_SET_ROLE = 2
    C_CREATE_ROLE = 3
    C_ADD_USER_TO_GROUP = 4
    C_CREATE_GROUP = 5
    C_CREATE_GROLE = 6
    C_ADD_GROLE = 7
    C_ADD_ROLE_TO_USER = 8
    # TODO: add more perms


def has_role_permissions(role_staff: int, *permissions: Permissions) -> bool:
    if role_staff % 2 == 1:
        return True
    for perm in permissions:
        if (role_staff >> perm.value) % 2 == 0:
            return False

    return True


db_user = UserDatabaseManager()
db_role = RoleDatabaseManager()

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
    """Хэширует пароль"""
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """Проверяет пароль и его хеш на равенство"""
    return password_context.verify(password, hashed_pass)


def create_token(
        subject: Union[str, Any], is_access=True, expires_delta: int = None
) -> str:
    """Генерирует jwt токен по данным и времени"""
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    elif is_access:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_exp = payload["exp"]
        token_sub = payload["sub"]

        if datetime.fromtimestamp(token_exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db_user.get_by_name(token_sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find user",
        )

    return user


def auth_user(*permissions: Permissions):
    async def wrapper(user: User = Depends(get_current_user)) -> User:
        """Авторизовывает пользователя по правам permissions"""

        result_mask = 0

        for role_name in user.roles:
            cur_role = await db_role.get_by_name(role_name)
            if cur_role is not None:
                result_mask |= cur_role.permissions

        if not has_role_permissions(result_mask, *permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User <{user.name}> has no required permission"
            )
        return user

    return wrapper
