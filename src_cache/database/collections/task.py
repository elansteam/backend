"""Определение класса Task"""
from typing import List
from src.settings import ObjectId
from pydantic import BaseModel


class Task(BaseModel):
    _id: ObjectId
    """Уникальный идентификатор объекта"""

    name: str
    """Название задачи"""

    tags: List[ObjectId]
    """Список тегов задачи"""

    difficult: int
    """Сложность задачи"""
