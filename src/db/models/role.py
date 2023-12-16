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

    @field_validator("role_code")
    def validate_role_code(self, value):
        """
        Validate role code
        Args:
            value: permission code
        Raises:
            ValidationError: if role code not positive
        """
        if value < 0:
            raise ValidationError("Role code must be positive")
        return value
