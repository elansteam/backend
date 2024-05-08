"""Contest related schemas"""

from pydantic import BaseModel, Field
from db.annotations import NameAnnotation, DescriptionAnnotation, DomainAnnotation, IntIdAnnotation


class ContestToCreate(BaseModel):
    """Group to create template"""

    name: NameAnnotation

    description: DescriptionAnnotation = Field("")

    domain: DomainAnnotation | None = Field(None)

    linked_group: IntIdAnnotation
