import datetime
from pydantic import Field

from utils.schemas import BaseModel
from .common import IntegerId, ObjectName, DomainName, ObjectDescription


class Contest(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-375"""

    id: IntegerId = Field(alias='_id')
    name: ObjectName
    domain: DomainName | None = None
    local_domain: DomainName | None = None
    description: ObjectDescription = ""
    submissions: list[IntegerId]
    members: list[IntegerId]
    creators: list[IntegerId]
    begin_time: datetime.datetime
    duration: datetime.datetime
    after_work: bool
    group_id: IntegerId
