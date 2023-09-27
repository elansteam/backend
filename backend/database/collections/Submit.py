"""Определение класса Submit"""
from typing import List, Dict
from datetime import datetime
from backend.project_types import ObjectId  # type: ignore
from pydantic import BaseModel


class Submit(BaseModel):
    id: ObjectId
    """Уникальный идентификатор объекта"""

    task: ObjectId
    """ID. Задача по которой посылка"""

    sender: ObjectId
    """ID. Отправитель посылки"""

    verdict: str
    """Вердикт суммарно по всей посылке"""

    time: datetime
    """Время, когда была отправлена посылка"""

    report: List[Dict[str, str]]
    """Список словарей, содержащих информацию о каждом тесте в посылке:\n
    test - номер теста\n
    verdict - вердикт для теста\n
    memory - использованная память
    time - время исполнения
    checkerOutput - дебаг вывод чекера (только для админов групп)\n
    input - входные данные (только для админов групп)\n
    output - выходные данные (только для админов групп)\n
    cerr - вывод потока cerr (только для админов групп)
    """
