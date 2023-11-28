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
    def validate_group_role_code(cls, value) -> None:
        """
        Validate role code
        Args:
            value: permission code
        Raises:
            ValidationError: if role code not positive
        """
        if value < 0:
            raise ValidationError("Group role code must be positive")
