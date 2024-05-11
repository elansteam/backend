"""Role definition"""
from pydantic import BaseModel, Field
from db.annotations import NameAnnotation, DescriptionAnnotation, \
    RoleCodeAnnotation, StrIdAnnotation


class Role(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-315"""

    id: StrIdAnnotation = Field(alias='_id')
    name: NameAnnotation
    description: DescriptionAnnotation
    role_code: RoleCodeAnnotation
