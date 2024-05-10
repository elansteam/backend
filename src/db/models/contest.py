"""Group definition"""
from pydantic import BaseModel, Field
from db.models.submission import Submission
from db.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
    DomainAnnotation


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

    problems: list[IntIdAnnotation] = Field([])

    submissions: list[Submission] = Field([])
