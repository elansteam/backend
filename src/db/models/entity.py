"""Domain entity representation in the database"""
from typing import Literal
from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation, DomainAnnotation


class Entity(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-395"""

    id: DomainAnnotation = Field(alias='_id')
    entity_type: Literal["user", "group", "contest", "reserve"]
    entity_id: IntIdAnnotation | None = Field(None)
