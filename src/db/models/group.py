"""Group definition"""
from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
    DomainAnnotation, StrIdAnnotation


class Group(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-335"""

    id: IntIdAnnotation = Field(alias='_id')
    name: NameAnnotation
    domain: DomainAnnotation | None = Field(None)
    description: DescriptionAnnotation
    members: list[IntIdAnnotation] = Field([])
    owner: IntIdAnnotation
    roles: list[StrIdAnnotation] = Field([])
