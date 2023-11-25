"""Group role definition"""
from pydantic import BaseModel, field_validator, ValidationError


class GroupRole(BaseModel):
    """GroupRole representation in database"""

    name: str
    """Role name"""

    description: str = ""
    """Role description"""

    role_code: int
    """Coded role permissions in byte representation"""

    group: str
    """Parent group name"""

    @field_validator("role_code")
    def validate_gpermission(cls, value) -> None:
        """
        Validate gpermission code
        if value < 0 -> exception
        Args:
            value: permission code
        """
        if value < 0:
            raise ValidationError("GPermissions must be positive")
