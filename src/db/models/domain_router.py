"""Domain router representation in the database"""
from typing import Literal
from pydantic import BaseModel, Field


class DomainRouter(BaseModel):
    """Domain router representation in the database"""

    id: str = Field(..., alias='_id')
    """Domain router domain"""

    entity_type: Literal["group"] | Literal["user"]
    """Type of the linked entity"""

    entity_id: int
    """ID of the linked entity"""
