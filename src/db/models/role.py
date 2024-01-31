"""Role definition"""
from pydantic import BaseModel, Field


class Role(BaseModel):
    """Role representation in database"""

    id: str = Field("__untitled", alias='_id')
    """Short string ID (e.g. 'admin'))"""

    name: str
    """Role name"""

    description: str
    """Role description"""

    role_code: int
    """Role representation in integer"""


class RoleCreate(BaseModel):
    """Model for interface to create role"""

    name: str
    """Role name"""

    description: str
    """Role description"""

    role_code: int
    """Role representation in integer"""


def role_name_to_id(role_name: str) -> str:
    """
    Converts role name to role id
    Args:
        role_name: role name to convert

    Returns: result id
    """
    return role_name.lower().replace(" ", "_")
