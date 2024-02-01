"""Role definition"""
from pydantic import BaseModel, Field, AfterValidator, ValidationError
from typing import Annotated


def not_negative(value: int) -> int:
    """
    Check if value is not negative
    Args:
        value: integer
    Returns:
        value
    Raises:
        ValidationError: if value is negative
    """
    if not value >= 0:
        raise ValueError("role code must be not negative")
    return value


NotNegative = Annotated[int, AfterValidator(not_negative)]  # custom type


class Role(BaseModel):
    """Role representation in database"""

    id: str = Field("__untitled", alias='_id')
    """Short string ID (e.g. 'admin'))"""

    name: str
    """Role name"""

    description: str
    """Role description"""

    role_code: NotNegative
    """Role representation in integer"""


class RoleCreate(BaseModel):
    """Model for interface to create role"""

    name: str
    """Role name"""

    description: str
    """Role description"""

    role_code: NotNegative
    """Role representation in integer"""


def role_name_to_id(role_name: str) -> str:
    """
    Converts role name to role id
    Args:
        role_name: role name to convert

    Returns: result id
    """
    return role_name.lower().replace(" ", "_")
