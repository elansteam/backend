import tempfile
from typing import Any

from _pytest.main import Session
from fastapi import APIRouter, Depends, UploadFile
from pathlib import Path  # FIXME КОСТЫЛЬ!!!

from pydantic import BaseModel

from auth.utils import auth_user
from db.models.annotations import IntIdAnnotation
from utils.response_utils import get_error_response, get_response, get_response_model, \
    get_error_schema
from db.models.problem import Problem
from db.models.submission import Submission, SubmissionToCreate
from db.models.user import User
import db
from config import Config
from loguru import logger
from datetime import datetime
from producer import produce_submission

router = APIRouter()


@router.post(
    "/create",
    response_model=get_response_model()
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
        solution_path=None,
        upload_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    produce_submission(created_submission_id)

    return get_response(await db.submission.get(created_submission_id))


class UserContestSubmissions(BaseModel):
    result: list[Submission]
    problem_names: list[str]  # FIXME set name annotation


@router.get(
    "/get_user_contest_submissions",
    response_model=get_response_model(UserContestSubmissions),
    responses={
        400: get_error_schema("Failed to retreive submissions")
    }
)
async def get_user_contest_submissions(
        user_id: IntIdAnnotation,
        contest_id: IntIdAnnotation,
        _current_user: User = Depends(auth_user())
) -> Any:
    contest = await db.contest.get(contest_id)

    if contest is None:
        return get_error_response("CONTEST_NOT_FOUND")

    user = db.user.get(user_id)

    if user is None:
        return get_error_response("USER_NOT_FOUND")

    result = await db.submission.get_all_submission_for_user_in_contest(user_id, contest_id)

    problem_names: list[str] = []  # FIXME set name annotation

    for submission in result:
        problem = await db.problem.get(submission.problem_id)
        if problem is None:
            problem_names.append("undefined")
        else:
            problem_names.append(problem.name)

    return get_response(UserContestSubmissions(result=result, problem_names=problem_names))
