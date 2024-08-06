from pydantic import Field

from utils.schemas import BaseModel
from .common import IntegerId, RoleCode


class GroupMember(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-415"""

    id: IntegerId = Field(alias="_id")
    group_id: IntegerId
    custom_permissions: RoleCode
    roles: list[IntegerId]
