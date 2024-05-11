"""Group role definition"""

from pydantic import BaseModel, Field
from db.annotations import NameAnnotation, DescriptionAnnotation, \
    RoleCodeAnnotation, StrIdAnnotation, IntIdAnnotation


class GroupRole(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-495"""

    id: StrIdAnnotation = Field(alias='_id')
    name: NameAnnotation
    description: DescriptionAnnotation
    group_id: IntIdAnnotation
    role_code: RoleCodeAnnotation
