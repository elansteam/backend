"""Group definition"""
from bson import ObjectId
from pydantic import BaseModel, Field


class Group(BaseModel):
    """Group representation in database"""
    id: ObjectId = Field(..., alias='_id')

    description: str
    """Group description"""

    members: dict[ObjectId, list[ObjectId]] = {}
    """Group members. Dict of user : list[ user group permissions ] """

    owner: ObjectId
    """Group owner name"""

    group_roles: list[ObjectId] = []
    """List of names group roles in group"""
