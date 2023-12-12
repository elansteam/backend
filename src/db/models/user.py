"""User definition and some useful stuff about user"""
from pydantic import BaseModel, Field
from utils.utils import ObjectId


class User(BaseModel):
    """User representation in database"""
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')
    domain_name: str
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
