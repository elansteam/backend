"""Group definition"""

import datetime
from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
    DomainAnnotation


class Contest(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-375"""

    id: IntIdAnnotation = Field(alias='_id')
    name: NameAnnotation
    domain: DomainAnnotation | None = None
    local_domain: DomainAnnotation | None = None
    description: DescriptionAnnotation = ""
    submissions: list[IntIdAnnotation]
    members: list[IntIdAnnotation]
    creators: list[IntIdAnnotation]
    begin_time: datetime.datetime
    duration: datetime.datetime
    after_work: bool
    group_id: IntIdAnnotation
