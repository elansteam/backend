"""Problem reprsentation in database"""
from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation, NameAnnotation


class Problem(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-455"""

    id: IntIdAnnotation = Field(alias='_id')
    name: NameAnnotation
