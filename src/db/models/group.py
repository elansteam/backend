"""Group definition"""
from bson import ObjectId
from pydantic import BaseModel, Field


class Group(BaseModel):
    """Group representation in database"""
    id: ObjectId = Field(..., alias='_id')

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
