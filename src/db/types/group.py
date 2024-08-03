from pydantic import Field

from utils.schemas import BaseModel
from .common import IntegerId, ObjectName, DomainName, StringId, ObjectDescription

class Group(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-335"""

    id: IntegerId = Field(alias='_id')
    name: ObjectName
    domain: DomainName | None = None
    description: ObjectDescription
    members: list[IntegerId] = []
    owner: IntegerId
    roles: list[StringId] = []
