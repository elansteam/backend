from typing import Literal
from pydantic import Field

from utils.schemas import BaseModel
from .common import IntegerId, DomainName

class Entity(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-395"""

    id: DomainName = Field(alias='_id')
    entity_type: Literal["user", "group", "contest", "reserve"]
    entity_id: IntegerId | None = None
