"""User related schemas"""

from pydantic import BaseModel, Field

from db.annotations import DomainAnnotation, EmailAnnotation

class UserSignupScheme(BaseModel):
    """Data for Signup user"""
    domain: DomainAnnotation | None = Field(None)
    password: str
    first_name: str
    last_name: str
    mid_name: str | None = Field(None)
    email: EmailAnnotation


class UserSigninScheme(BaseModel):
    """Data for user signin"""
    login: str
    password: str
