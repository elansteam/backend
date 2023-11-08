from pydantic import BaseModel, EmailStr
from src.db.oid import OID
from bson import ObjectId
from typing import List
from .role import Role


class User(BaseModel):
    """Модель пользователя в базе данных"""

    _id: ObjectId
    """Уникальный идентификатор пользователя"""

    user_name: str
    """Идентификатор пользователя"""

    password_hash: str
    """SHA-256 хеш пароля"""

    # email: EmailStr | None # TODO: add in future
    # """Уникальный адрес электронной почты"""

    first_name: str
    """Имя"""

    last_name: str
    """Фамилия"""

    mid_name: str | None
    """Отчество"""

    roles: List[str] = []
    """Список ролей пользователя по их именам"""

    # TODO: ADD BELOW IN FUTURE

    # groups: List[ObjectId]
    # """Группы, в которых состоит пользователь"""

    # # permission: int
    # # """Уровень доступа пользователя:
    # # 0 - Нулевой
    # # 1 - Пользователь может создавать группы
    # # 3 - Пользователь может создавать задачи
    # # 2 - Пользователь админ"""


class UserSignup(BaseModel):
    """Представление пользователя для его создания"""
    user_name: str
    password: str
    first_name: str
    last_name: str
    mid_name: str | None = None
    # email: EmailStr | None = None # TODO: add in future


class UserSignin(BaseModel):
    """Представление пользователя для авторизации"""
    user_name: str
    password: str
