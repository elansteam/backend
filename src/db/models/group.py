from pydantic import BaseModel


class Group(BaseModel):
    """Представление группы в базе данных"""

    name: str
    """Уникальное имя группы"""

    description: str
    """Описание группы"""

    members: dict[str, list[str]] = {}
    """Словарь пользователь : список ролей"""

    owner: str
    """user_name пользователя, создавшего группу"""

    groles: list[str] = []
    """Список ролей созданных в этой группе"""
