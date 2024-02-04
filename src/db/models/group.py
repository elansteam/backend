"""Group definition"""
from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
    DomainAnnotation


class Group(BaseModel):
    """Group representation in database"""
    id: IntIdAnnotation = Field(alias='_id')

    name: NameAnnotation
    """Group name"""

    description: DescriptionAnnotation = Field("")
    """Group description"""

    domain: DomainAnnotation | None = Field(None)
    """Group domain"""

    members: dict[int, tuple[int, list[str]]] = {}
    """Group members"""

    owner: IntIdAnnotation
    """User ID of group owner"""

    group_roles: dict[str, int] = Field({})
    """List of names group roles in group"""
