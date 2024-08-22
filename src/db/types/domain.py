from typing import Literal
from pydantic import Field

from utils.schemas import BaseModel


TargetType = Literal["user", "group", "contest"]

class Entity(BaseModel):
    id: str = Field(alias='_id')
    target_type: TargetType
    target_id: int
