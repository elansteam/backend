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
    def validate_role_code(cls, value):
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
