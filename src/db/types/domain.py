from typing import Literal
from pydantic import Field

from utils.schemas import BaseModel


TargetType = Literal["user", "group", "contest"]

class Entity(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-395"""

    id: str = Field(alias='_id')
    target_type: TargetType
    target_id: int
