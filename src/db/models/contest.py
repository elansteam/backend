"""Group definition"""
from datetime import datetime

from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
    DomainAnnotation, RoleCodeAnnotation, StrIdAnnotation


class Submission(BaseModel):
    """User submission"""

    # id: IntIdAnnotation = Field(alias="")
    upload_time: datetime
    code_text: str
    status: str | None = None
    target_problem_id: IntIdAnnotation


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


class ContestToCreate(BaseModel):
    """Group to create template"""

    name: NameAnnotation

    description: DescriptionAnnotation = Field("")

    domain: DomainAnnotation | None = Field(None)

    linked_group: IntIdAnnotation
