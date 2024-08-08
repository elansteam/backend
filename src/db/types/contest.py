import datetime
from pydantic import Field

from utils.schemas import BaseModel


class Contest(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-375"""

    id: int = Field(alias='_id')
    name: str
    domain: str | None = None
    local_domain: str | None = None
    description: str = ""
    submissions: list[int]
    members: list[int]
    creators: list[int]
    begin_time: datetime.datetime
    duration: datetime.datetime
    after_work: bool
    group_id: int
