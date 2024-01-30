"""Role definition"""
from pydantic import BaseModel, field_validator, ValidationError, Field


class Role(BaseModel):
    """Role representation in database"""

    id: str = Field(..., alias='_id')
    """Short string ID (e.g. 'admin'))"""

    name: str
    """Role name"""

    description: str
    """Role description"""

    role_code: int
    """Role representation in integer"""
