from pydantic import Field

from utils.schemas import BaseModel
from .common import IntegerId


class ContestMember(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-435"""

    id: IntegerId = Field(alias="_id")
    contest_id: IntegerId
