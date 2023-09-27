"""Определение класса Group"""
from typing import List
from dataclasses import dataclass, field
from ...project_types import ObjectId  # type: ignore
from pydantic import BaseModel


class Group(BaseModel):
    id: ObjectId
    """Уникальный идентификатор объекта"""

    name: str
    """Имя группы"""

    description: str
    """Описание группы"""

    owner: ObjectId
    """Создатель группы"""

    members: List[ObjectId]
    """Список участников группы"""

    admins: List[ObjectId]
    """Список администраторов группы"""

    contests: List[ObjectId]
    """Контесты группы"""
