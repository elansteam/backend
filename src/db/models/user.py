"""User definition and some useful stuff about user"""
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from utils import PydanticObjectId


class User(BaseModel):
    """User representation in database"""
    id: PydanticObjectId = Field(..., alias='_id')
    password_hash: str
    first_name: str
    last_name: str
    mid_name: str | None
    roles: list[ObjectId] = Field([])
    """List of global roles, which user have"""


class UserSignup(BaseModel):
    """Data for Signup user"""
    name: str
    password: str
    first_name: str
    last_name: str
    mid_name: str | None = None


class UserSignin(BaseModel):
    """Data for user signin"""
    name: str
    password: str
