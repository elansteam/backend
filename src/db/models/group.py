from pydantic import BaseModel
from typing import List, Dict
from config import Config


class Group(BaseModel):
    """Представление группы в базе данных"""

    name: str
    """Уникальное имя группы"""

    description: str
    """Описание группы"""

    members: Dict[str, str] = {}
    """Словарь пользователь : роль"""

    owner: str
    """user_name пользователя, создавшего группу"""

    groles: List[str] = []
    """Список ролей созданных в этой группе"""
