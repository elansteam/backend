"""Group definition"""
from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
    DomainAnnotation, RoleCodeAnnotation, StrIdAnnotation


class Contest(BaseModel):
    """Group representation in database"""
    id: IntIdAnnotation = Field(alias='_id')
    """Group id"""

    name: NameAnnotation
    """Group name"""

    description: DescriptionAnnotation = Field("")
    """Group description"""

    domain: DomainAnnotation | None = Field(None)
    """Group domain"""

    linked_group: IntIdAnnotation
    """Linked group"""

    tasks: list[IntIdAnnotation] = Field([])


class ContestToCreate(BaseModel):
    """Group to create template"""

    name: NameAnnotation

    description: DescriptionAnnotation = Field("")

    domain: DomainAnnotation | None = Field(None)

    linked_group: IntIdAnnotation
