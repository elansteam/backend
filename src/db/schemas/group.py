"""Group related schemas"""

from pydantic import BaseModel, Field
from db.annotations import NameAnnotation, DescriptionAnnotation, DomainAnnotation, IntIdAnnotation

class GroupToCreate(BaseModel):
    """Group to create template"""

    name: NameAnnotation

    description: DescriptionAnnotation = Field("")

    domain: DomainAnnotation | None = Field(None)

    members: list[IntIdAnnotation] = Field([])
    """Who will be in group"""
