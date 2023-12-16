"""Group role definition"""
from pydantic import BaseModel, field_validator, ValidationError, Field


class GroupRole(BaseModel):
    """GroupRole representation in database"""

    id: str = Field(..., alias='_id')
    """Group ID + string ID (e.g. 'group1_admin'))"""

    name: str
    """Role name"""

    description: str = ""
    """Role description"""

    role_code: int
    """Encoded role permissions representation"""

    group: int
    """ID of the group to which the role belongs"""

    @field_validator("role_code")
    def validate_group_role_code(self, value) -> None:
        """
        Validate role code
        Args:
            value: permission code
        Raises:
            ValidationError: if role code not positive
        """
        if value < 0:
            raise ValidationError("Group role code must be positive")
