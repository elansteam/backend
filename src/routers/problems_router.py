import tempfile
from typing import Any

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel
from starlette.responses import FileResponse

from auth.utils import auth_user
from utils.response_utils import get_error_response, get_response, get_response_model, \
    get_error_schema
from db.models.problem import Problem
from db.models.user import User
import db
from db.models.annotations import NameAnnotation, IntIdAnnotation
from config import Config

import os

router = APIRouter()


class Addproblem(BaseModel):
    created_problem_id: IntIdAnnotation


@router.post(
    "/create",
    response_model=get_response_model(Addproblem)
)
async def create_problem(name: NameAnnotation, problem_archive: UploadFile, _current_user: User = Depends(
    auth_user()
)) -> Any:
    """Add a problem to contest by zip"""

    #  TODO: add creating directory for problems
    # with tempfile.NamedTemporaryFile() as file_object:
    #     with open(file_object.name, "wb") as file_object1:
    #         file_object1.write(await problem_archive.read())
    #     with ZipFile(file_object1.name, "r") as zip_file:
    #         with zip_file.open("css/tokens.css", "r") as theme_file:
    #             print(str(theme_file.read()))

    # creating problem object
    problem_to_create = Problem(
        _id=1,  # not used
        name=name
    )
    created_problem_id = await db.problem.insert_with_id(problem_to_create)
    response = Addproblem(created_problem_id=created_problem_id)
    return get_response(response)


@router.get(
    "/get_legend"
)
async def get_problem_legend(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive problem legend"""

    try:
        to_return = FileResponse(path=f'{Config.elan_path}/problems/problem{_id}/legend.mdx', filename="legend.mdx",
                                 media_type='multipart/form-data')
        print(to_return)
        return to_return
    except Exception as e:
        print("Exception", e)
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_input"
)
async def get_problem_input(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive problem legend"""

    try:
        to_return = FileResponse(path=f'{Config.elan_path}/problems/problem{_id}/input.mdx', filename="input.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_output"
)
async def get_problem_output(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive problem legend"""

    try:
        to_return = FileResponse(path=f'{Config.elan_path}/problems/problem{_id}/output.mdx', filename="output.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_scoring"
)
async def get_problem_scoring(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive problem legend"""

    try:
        to_return = FileResponse(path=f'{Config.elan_path}/problems/problem{_id}/scoring.mdx', filename="scoring.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_notes"
)
async def get_notes(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive problem legend"""

    try:
        to_return = FileResponse(path=f'{Config.elan_path}/problems/problem{_id}/notes.mdx', filename="notes.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_name"
)
async def get_name(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())) -> Any:
    """Retreive problem name by problem id"""

    problem = await db.problem.get(_id)

    if problem is None:
        return get_error_response("PROBLEM_NOT_FOUND")

    return problem.name


class Examples(BaseModel):

    input: list[str]
    output: list[str]

@router.get(
    "/get_examples",
    response_model=get_response_model(Examples),
    responses={
        400: get_error_schema("Failed to retreive problem examples.")
    }
)
async def get_examples(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())) -> Any:
    directory = f"{Config.elan_path}/problems/problem{_id}/"

    result = Examples(input=[], output=[])

    for filename in os.scandir(directory):
        if filename.is_file():
            if filename.name.startswith("example") and not filename.name.endswith(".a"):
                with open(filename.path, "r") as file:
                    result.input.append(file.read())
                with open(filename.path+".a", "r") as file:
                    result.output.append(file.read())

    return get_response(result)

