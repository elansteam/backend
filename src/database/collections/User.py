"""Определение класса User"""
from typing import List
from src.helpers.config import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    _id: ObjectId
    """Уникальный идентификатор объекта"""

    user_name: str
    """Идентификатор пользователя"""

    password_hash: str
    """SHA-256 хеш пароля"""

    first_name: str
    """Имя"""

    last_name: str
    """Фамилия"""

    mid_name: str | None
    """Отчество"""

    groups: List[ObjectId]
    """Группы, в которых состоит пользователь"""

    permission: int
    """Уровень доступа пользователя:
    0 - Нулевой
    1 - Пользователь может создавать группы
    3 - Пользователь может создавать задачи  
    2 - Пользователь админ"""

