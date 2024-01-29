"""User definition and some useful stuff about user"""
from pydantic import BaseModel, Field


class User(BaseModel):
    """User representation in database"""
    id: int = Field(-1, alias='_id')
    email: str
    domain: str | None = Field(None)
    password_hash: str
    first_name: str
    last_name: str
    mid_name: str | None = Field(None)
    roles: list[str] = Field([])
    """List of global roles, which user have"""


class UserSignup(BaseModel):
    """Data for Signup user"""
    password: str
    first_name: str
    last_name: str
    mid_name: str | None = None


class UserSignin(BaseModel):
    """Data for user signin"""
    login: str
    password: str
