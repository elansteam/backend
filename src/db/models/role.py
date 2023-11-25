"""Role definition"""
from pydantic import BaseModel, field_validator, ValidationError


class Role(BaseModel):
    """Role representation in database"""

    name: str
    """Role name"""

    description: str
    """Role description"""

    role_code: int
    """Role representation in integer"""

    @field_validator("role_code")
    def my_custom_validator(cls, value):
        """
        Validate role code
        if value < 0 -> exception
        Args:
            value: permission code
        """
        if value < 0:
            raise ValidationError("Role code must be positive")
        return value
