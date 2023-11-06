"""Определение класса Contest"""
from typing import List, Tuple
from datetime import datetime
from src.settings import ObjectId
from pydantic import BaseModel


class Contest(BaseModel):
    _id: ObjectId
    """Уникальный идентификатор объекта"""

    name: str
    """Имя контеста"""

    description: str
    """Описание контеста"""

    task_set: List[Tuple[ObjectId, int]]
    """Список задач в совокупности с их баллами"""

    status: int
    """Статус контеста в кодовом значении:
    0 - не начался
    1 - идет
    2 - закончился, идет дорешка
    3 - закончился, дорешки нет
    """

    start_time: datetime
    """Время начала контеста"""

    end_time: datetime
    """Время конца контеста"""

    group: ObjectId
    """Группа, к которой привязан контест"""
