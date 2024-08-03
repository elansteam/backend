from pydantic import Field

from utils.schemas import BaseModel
from .common import StringId, ObjectName, ObjectDescription, RoleCode

class Role(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-315"""

    id: StringId = Field(alias='_id')
    name: ObjectName
    description: ObjectDescription
    role_code: RoleCode
