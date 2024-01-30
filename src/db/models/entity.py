"""Domain router representation in the database"""
from typing import Literal
from pydantic import BaseModel, Field


class Entity(BaseModel):
    """Domain router representation in the database"""

    id: str = Field("", alias='_id')
    """Domain router domain"""

    entity_type: Literal["group"] | Literal["user"] | Literal["reserve"]
    """Type of the linked entity"""

    entity_id: int = Field(-1)
    """ID of the linked entity"""
