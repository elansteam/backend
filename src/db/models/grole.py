from pydantic import BaseModel
from typing import List


class GRole(BaseModel):
    """Представление роли конкретно в группе"""

    name: str
    """Имя роли"""

    description: str
    """Описание роли"""

    permissions: List[str]
    """Список разрешений"""
