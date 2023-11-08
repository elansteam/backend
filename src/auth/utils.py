import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

# TODO: set to env variables!!!!
JWT_SECRET_KEY = "jwt_secret_key"  # should be kept secret
JWT_REFRESH_SECRET_KEY = "jwt_refresh_secret_key"  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
