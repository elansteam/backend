"""User definition and some useful stuff about user"""
from pydantic import BaseModel, Field


class User(BaseModel):
    """Модель пользователя в базе данных"""

    name: str

    password_hash: str

    first_name: str

    last_name: str

    mid_name: str | None

    roles: list[str] = Field([])
    """List of global roles, which user have"""


class UserSignup(BaseModel):
    """Data for Signup user"""
    name: str
    password: str
    first_name: str
    last_name: str
    mid_name: str | None = None


class UserSignin(BaseModel):
    """Data for user signin"""
    name: str
    password: str
