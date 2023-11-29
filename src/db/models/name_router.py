"""Name router representation"""
from pydantic import BaseModel
from bson.objectid import ObjectId


class NameRouter(BaseModel):
    """Name router"""

    object_id: ObjectId
    """Id of target object"""

    name: str
    """object name"""

    collection: str
    """Collection name of target object"""
