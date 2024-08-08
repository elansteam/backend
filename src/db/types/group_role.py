from pydantic import Field

from utils.schemas import BaseModel


class GroupRole(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-495"""

    id: str = Field(alias='_id')
    name: str
    description: str
    group_id: int
    role_code: int
