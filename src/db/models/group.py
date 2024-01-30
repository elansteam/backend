"""Group definition"""
from pydantic import BaseModel, Field


class Group(BaseModel):
    """Group representation in database"""
    id: int = Field(-1, alias='_id')

    name: str
    """Group name"""

    description: str = Field("")
    """Group description"""

    domain: str | None = Field(None)
    """Group domain"""

    members: dict[int, tuple[int, list[str]]] = {}
    """Group members"""

    owner: int
    """User ID of group owner"""

    group_roles: dict[str, int] = Field(dict())
    """List of names group roles in group"""
