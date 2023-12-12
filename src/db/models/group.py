"""Group definition"""
from typing import Annotated

from pydantic import BaseModel, Field
from utils.utils import ObjectId


class Group(BaseModel):
    """Group representation in database"""
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')

    description: str
    """Group description"""

    members: dict[ObjectId, list[ObjectId]] = {}
    """Group members. Dict of user : list[ user group permissions ] """

    owner: ObjectId
    """Group owner name"""

    group_roles: list[ObjectId] = []
    """List of names group roles in group"""
