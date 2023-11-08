from pydantic import BaseModel


class Permission(BaseModel):
    """Представление права доступа"""
    name: str
    description: str
