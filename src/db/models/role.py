"""Role definition"""
from pydantic import BaseModel, Field
from db.models.annotations import NameAnnotation, DescriptionAnnotation, \
    RoleCodeAnnotation, StrIdAnnotation


class Role(BaseModel):
    """Role representation in database"""

    id: StrIdAnnotation = Field(alias='_id')
    """Short string ID (e.g. 'admin'))"""

    name: NameAnnotation
    """Role name"""

    description: DescriptionAnnotation
    """Role description"""

    role_code: RoleCodeAnnotation
    """Role representation in integer"""
