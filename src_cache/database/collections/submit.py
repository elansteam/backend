"""Определение класса Submit"""
from typing import List, Dict
from datetime import datetime
from src.settings import ObjectId
from pydantic import BaseModel, Json


class Submit(BaseModel):
    _id: ObjectId
    """Уникальный идентификатор объекта"""

    task: ObjectId
    """ID. Задача по которой посылка"""

    sender: ObjectId
    """ID. Отправитель посылки"""

    verdict: str
    """Вердикт суммарно по всей посылке"""

    time: datetime
    """Время, когда была отправлена посылка"""

    report: Json
    """Список словарей, содержащих информацию о каждом тесте в посылке:
    test - номер теста
    verdict - вердикт для теста
    memory - использованная память
    time - время исполнения
    checkerOutput - дебаг вывод чекера (только для админов групп)
    input - входные данные (только для админов групп)
    output - выходные данные (только для админов групп)
    cerr - вывод потока cerr (только для админов групп)
    """
