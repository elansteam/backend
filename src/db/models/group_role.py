"""Group role definition"""
from pydantic import BaseModel, field_validator, ValidationError, Field
from utils.utils import ObjectId


class GroupRole(BaseModel):
    """GroupRole representation in database"""

    id: ObjectId = Field(..., alias='_id')

    description: str = ""
    """Role description"""

    role_code: int
    """Coded role permissions in byte representation"""

    group: ObjectId
    """Parent group id"""

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
