import datetime
from typing import Literal
from pydantic import Field

from utils.schemas import BaseModel

class Submission(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-475"""

    id: int = Field(alias="_id")
    problem_id: int
    contest_id: int
    user_id: int
    solution_path: str | None = None
    status: Literal["Testing", "OK"]
    upload_time: datetime.datetime
