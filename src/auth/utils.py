from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from starlette import status
from db.managers.user_database_manager import UserDatabaseManager
from db.models.user import User
from starlette.responses import JSONResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

# TODO: set to env variables!!!!
JWT_SECRET_KEY = "jwt_secret_key"  # should be kept secret
JWT_REFRESH_SECRET_KEY = "jwt_refresh_secret_key"  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = UserDatabaseManager()

AUTH_RESPONSE_MODEL = {
    "description": "Failed auth",
    "content": {
        "application/json": {
            "example": {"detail": [
                {"msg": "Auth failed"}
            ]},
        }
    }
}

AUTH_FAILED = JSONResponse(status_code=401, content={"detail": [
    {"msg": "Auth failed"}
]})


def get_hashed_password(password: str) -> str:
    """Хэширует пароль"""
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """Проверяет пароль и его хеш на равенство"""
    return password_context.verify(password, hashed_pass)


def create_token(subject: Union[str, Any], is_access=True, expires_delta: int = None) -> str:
    """Генерирует jwt токен по данным и времени"""
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    elif is_access:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str) -> User:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db.get_by_name(token_sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
