from pydantic import Field

from utils.schemas import BaseModel
from .common import StringId, ObjectName, ObjectDescription, IntegerId, RoleCode

class GroupRole(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-495"""

    id: StringId = Field(alias='_id')
    name: ObjectName
    description: ObjectDescription
    group_id: IntegerId
    role_code: RoleCode
