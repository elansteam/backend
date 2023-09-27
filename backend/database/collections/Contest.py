"""Определение класса Contest"""
from typing import List, Tuple
from datetime import datetime
from ...project_types import ObjectId  # type: ignore
from pydantic import BaseModel


class Contest(BaseModel):
    id: ObjectId
    """Уникальный идентификатор объекта"""

    name: str
    """Имя контеста"""

    description: str
    """Описание контеста"""

    task_set: List[Tuple[ObjectId, int]]
    """Список задач в совокупности с их баллами"""

    status: int
    """Статус контеста в кодовом значении: \n
    0 - не начался\n
    1 - идет\n
    2 - закончился, идет дорешка\n
    3 - закончился, дорешки нет\n
    """

    start_time: datetime
    """Время начала контеста"""

    end_time: datetime
    """Время конца контеста"""

    group: ObjectId
    """Группа, к которой привязан контест"""
