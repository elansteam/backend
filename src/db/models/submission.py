from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, AfterValidator
from db.models.annotations import IntIdAnnotation


class SubmissionToCreate(BaseModel):

    problem_id: IntIdAnnotation

    contest_id: IntIdAnnotation

    solution: str


class Submission(BaseModel):

    id: IntIdAnnotation = Field(alias="_id")

    problem_id: IntIdAnnotation

    contest_id: IntIdAnnotation

    user_id: IntIdAnnotation

    solution_path: str | None = None

    status: str | None = None

    upload_time: str
