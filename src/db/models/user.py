"""User definition and some useful stuff about user"""
from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation, DomainAnnotation, EmailAnnotation, \
    StrIdAnnotation


class User(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-295"""

    id: IntIdAnnotation = Field(alias='_id')
    domain: DomainAnnotation | None = Field(None)
    password_hash: str
    first_name: str
    last_name: str
    mid_name: str | None = Field(None)
    groups: list[IntIdAnnotation] = Field([])
    roles: list[StrIdAnnotation] = Field([])
    email: EmailAnnotation | None
