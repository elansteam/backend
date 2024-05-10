"""User definition and some useful stuff about user"""
from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation, DomainAnnotation, EmailAnnotation, \
    StrIdAnnotation


class User(BaseModel):
    """User representation in database"""
    id: IntIdAnnotation = Field(alias='_id')
    email: EmailAnnotation
    domain: DomainAnnotation | None = Field(None)
    password_hash: str
    first_name: str
    last_name: str
    mid_name: str | None = Field(None)
    roles: list[StrIdAnnotation] = Field([])
    """List of global roles, which user have"""
