"""Domain node representation in database"""
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from utils import PydanticObjectId


class DomainNode(BaseModel):
    """Domain node representation in database"""

    id: PydanticObjectId = Field(..., alias='_id')

    target_id: ObjectId
    """Id of target object"""

    target_name: str
    """target object domain or name"""

    target_collection: str
    """Collection name of target object"""
