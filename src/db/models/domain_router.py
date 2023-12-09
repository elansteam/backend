"""Domain router representation in database"""
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class DomainRouter(BaseModel):
    """Domain router representation in database"""

    id: ObjectId = Field(..., alias='_id')

    target_id: ObjectId
    """Id of target object"""

    target_name: str
    """target object domain or name"""

    target_collection: str
    """Collection name of target object"""
