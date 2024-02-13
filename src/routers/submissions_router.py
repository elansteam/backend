import tempfile
from typing import Any

from _pytest.main import Session
from fastapi import APIRouter, Depends, UploadFile
from pathlib import Path  # FIXME КОСТЫЛЬ!!!

from auth.utils import auth_user
from utils.response_utils import get_error_response, get_response, get_response_model, \
    get_error_schema
from db.models.problem import Problem
from db.models.submission import Submission, SubmissionToCreate
from db.models.user import User
import db
from config import Config
from loguru import logger


router = APIRouter()


@router.post(
    "/create",
    response_model=get_response_model(Submission)
)
async def create_submission(
        to_create: SubmissionToCreate,
        _current_user: User = Depends(auth_user())
) -> Any:
    """Creating submission and sent it to rabbitMQ"""

    contest = await db.contest.get(to_create.contest_id)
    if contest is None:
        return get_error_response("CONTEST_NOT_FOUND")

    if await db.problem.get(to_create.problem_id) is None:
        return get_error_response("PROBLEM_NOT_FOUND")

    submission = Submission(
        _id=1,  # not used FIXME
        contest_id=to_create.contest_id,
        problem_id=to_create.problem_id,
        user_id=_current_user.id,
        status=None,
        solution_path=None
    )

    created_submission_id = await db.submission.insert_with_id(submission)

    solution_directory = Config.elan_path + (f"/submissions"
                                             f"/contest{contest.id}"
                                             f"/submission{created_submission_id}")

    Path(solution_directory).mkdir(parents=True, exist_ok=True)

    solution_path = solution_directory + "/solution.cpp"  # FIXME it only cpp making banana

    with open(solution_path, "w") as solution:
        solution.write(to_create.solution)

    await db.submission.attach_solution_path(created_submission_id, solution_path)

    return get_response(await db.submission.get(created_submission_id))
