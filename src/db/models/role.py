"""Role definition"""
from typing import Annotated
from pydantic import BaseModel, Field, AfterValidator
from db.models.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
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


class RoleCreate(BaseModel):
    """Model for interface to create role"""

    name: NameAnnotation
    """Role name"""

    description: DescriptionAnnotation
    """Role description"""

    role_code: RoleCodeAnnotation
    """Role representation in integer"""


def role_name_to_id(role_name: str) -> str:
    """
    Converts role name to role id
    Args:
        role_name: role name to convert

    Returns: result id
    """
    return role_name.lower().replace(" ", "_")
