"""Submission model"""

from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation


class Submission(BaseModel):

    id: IntIdAnnotation = Field(alias="_id")

    problem_id: IntIdAnnotation

    contest_id: IntIdAnnotation

    user_id: IntIdAnnotation

    solution_path: str | None = None

    status: str | None = None

    upload_time: str
