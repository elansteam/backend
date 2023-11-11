from pydantic import BaseModel


class GPermission(BaseModel):
    """Представление права доступа в локальной группе"""

    name: str
    """Имя права"""

    description: str
    """Описание права"""
