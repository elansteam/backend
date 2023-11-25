"""Group definition"""
from pydantic import BaseModel


class Group(BaseModel):
    """Group representation in database"""

    name: str
    """Group name"""

    description: str
    """Group description"""

    members: dict[str, list[str]] = {}
    """Group members"""

    owner: str
    """Group owner name"""

    group_roles: list[str] = []
    """List of names group roles in group"""
