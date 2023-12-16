"""Group definition"""
from pydantic import BaseModel, Field


class Group(BaseModel):
    """Group representation in database"""
    id: int = Field(..., alias='_id')

    name: str
    """Group name"""

    description: str
    """Group description"""

    domain: str | None
    """Group domain"""

    members: dict[int, list[str]] = {}
    """Group members"""

    owner: int
    """User ID of group owner"""

    group_roles: list[str] = []
    """List of names group roles in group"""
