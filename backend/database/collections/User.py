"""Определение класса User"""
from typing import List
from dataclasses import dataclass, field
from ...project_types import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    id: ObjectId
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
