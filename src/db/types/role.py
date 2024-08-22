from pydantic import Field

from utils.schemas import BaseModel


class Role(BaseModel):
    id: str = Field(alias='_id')
    name: str
    description: str | None = None
    code: int
