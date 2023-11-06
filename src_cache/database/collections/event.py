"""Определение класса Task"""
import datetime
from typing import List
from src.settings import ObjectId
from pydantic import BaseModel, Json


class Event(BaseModel):
    _id: ObjectId
    """Уникальный идентификатор объекта"""

    creation_time: datetime.datetime
    """Время создания события"""

    tags: List[str]
    """Список тегов"""

    data: Json
    """Данные события"""
