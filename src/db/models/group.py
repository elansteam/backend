"""Group definition"""
from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel, Field
from utils.PydanticObjectId import PydanticObjectId


class Group(BaseModel):
    """Group representation in database"""
    id: PydanticObjectId = Field(..., alias='_id')

    description: str
    """Group description"""

    members: dict[ObjectId, list[ObjectId]] = {}
    """Group members. Dict of user : list[ user group permissions ] """

    owner: ObjectId
    """Group owner name"""

    group_roles: list[ObjectId] = []
    """List of names group roles in group"""
