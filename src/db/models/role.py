from pydantic import BaseModel
from typing import List
from .permission import Permission


class Role(BaseModel):
    """Представление роли пользователя, роль - совокупность permissions"""
    name: str
    description: str
    permissions: List[Permission]
