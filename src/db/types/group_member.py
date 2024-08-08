from pydantic import Field

from utils.schemas import BaseModel


class GroupMember(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-415"""

    id: int = Field(alias="_id")
    group_id: int
    custom_role_code: int
    roles: list[int]
