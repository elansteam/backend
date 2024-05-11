"""Submission model"""

import datetime
from typing import Literal
from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation


class Submission(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-475"""
    id: IntIdAnnotation = Field(alias="_id")
    problem_id: IntIdAnnotation
    contest_id: IntIdAnnotation
    user_id: IntIdAnnotation
    solution_path: str | None = None
    status: Literal["Testing", "OK"]
    upload_time: datetime.datetime
