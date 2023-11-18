from pydantic import BaseModel, Field
from bson import ObjectId


class User(BaseModel):
    """Модель пользователя в базе данных"""

    _id: ObjectId
    """Уникальный идентификатор пользователя"""

    name: str
    """Идентификатор пользователя"""

    password_hash: str
    """SHA-256 хеш пароля"""

    first_name: str
    """Имя"""

    last_name: str
    """Фамилия"""

    mid_name: str | None
    """Отчество"""

    roles: list[str]
    """Список ролей пользователя по их именам"""


class UserSignup(BaseModel):
    """Представление пользователя для его создания"""
    name: str
    password: str
    first_name: str
    last_name: str
    mid_name: str | None = None


class UserSignin(BaseModel):
    """Представление пользователя для авторизации"""
    name: str
    password: str
