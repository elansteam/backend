from pydantic import Field

from utils.schemas import BaseModel

class Role(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-315"""

    id: str = Field(alias='_id')
    name: str
    description: str = ""
    code: int
