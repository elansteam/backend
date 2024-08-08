from pydantic import Field

from utils.schemas import BaseModel


class Group(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-335"""

    id: int = Field(alias='_id')
    name: str
    domain: str | None = None
    description: str
    members: list[int] = []
    owner_id: int
    roles: list[str] = []
