"""Определение класса Group"""
from typing import List
from src.helpers.config import ObjectId
from pydantic import BaseModel


class Group(BaseModel):
    _id: ObjectId
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
