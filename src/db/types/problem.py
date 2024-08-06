from pydantic import Field

from utils.schemas import BaseModel
from .common import IntegerId, ObjectName

class Problem(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-455"""

    id: IntegerId = Field(alias='_id')
    name: ObjectName
