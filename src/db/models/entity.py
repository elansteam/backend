"""Domain router representation in the database"""
from typing import Literal
from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation, DomainAnnotation


class Entity(BaseModel):
    """Domain router representation in the database"""

    id: DomainAnnotation = Field(alias='_id')
    """Domain router domain"""

    entity_type: Literal["group"] | Literal["user"] | Literal["reserve"]
    """Type of the linked entity"""

    entity_id: IntIdAnnotation | None = Field(None)
    """ID of the linked entity"""
