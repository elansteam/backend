"""Group member reprentation in databas"""

from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation, RoleCodeAnnotation


class GroupMember(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-415"""

    id: IntIdAnnotation = Field(alias="_id")
    group_id: IntIdAnnotation
    custom_permissions: RoleCodeAnnotation
    roles: list[IntIdAnnotation]
