"""Определение класса Task"""
from typing import List
from ...project_types import ObjectId  # type: ignore
from pydantic import BaseModel


class Task(BaseModel):
    id: ObjectId
    """Уникальный идентификатор объекта"""

    name: str
    """Название задачи"""

    tags: List[ObjectId]
    """Список тегов задачи"""

    difficult: int
    """Сложность задачи"""
