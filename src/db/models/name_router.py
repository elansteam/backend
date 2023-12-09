"""Name router representation in the database"""
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class NameRouter(BaseModel):
    """Name router representation in the database"""

    id: ObjectId = Field(..., alias='_id')

    object_id: ObjectId
    """Id of target object"""

    name: str
    """object name"""

    collection: str
    """Collection name of target object"""
