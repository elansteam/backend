"""Submission related schemas"""

from pydantic import BaseModel
from db.annotations import IntIdAnnotation

class SubmissionToCreate(BaseModel):
    """Scheme for creating a submission"""

    problem_id: IntIdAnnotation

    contest_id: IntIdAnnotation

    solution: str
