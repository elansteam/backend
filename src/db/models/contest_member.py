"""Contest member reprentation in databas"""

from pydantic import BaseModel, Field
from db.annotations import IntIdAnnotation


class ContestMember(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-435"""

    id: IntIdAnnotation = Field(alias="_id")
    contest_id: IntIdAnnotation
