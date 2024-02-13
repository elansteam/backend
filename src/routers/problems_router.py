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

router = APIRouter()


class AddTask(BaseModel):
    created_task_id: IntIdAnnotation


@router.post(
    "/create",
    response_model=get_response_model(AddTask)
)
async def create_task(name: NameAnnotation, task_archive: UploadFile, _current_user: User = Depends(
    auth_user()
)) -> Any:
    """Add a task to contest by zip"""

    #  TODO: add creating directory for tasks
    # with tempfile.NamedTemporaryFile() as file_object:
    #     with open(file_object.name, "wb") as file_object1:
    #         file_object1.write(await task_archive.read())
    #     with ZipFile(file_object1.name, "r") as zip_file:
    #         with zip_file.open("css/tokens.css", "r") as theme_file:
    #             print(str(theme_file.read()))

    # creating task object
    task_to_create = Problem(
        _id=1,  # not used
        name=name
    )
    created_task_id = await db.problem.insert_with_id(task_to_create)
    response = AddTask(created_task_id=created_task_id)
    return get_response(response)


@router.get(
    "/get_legend"
)
async def get_task_legend(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive task legend"""

    try:
        to_return = FileResponse(path=f'./data/problems/{_id}/legend.mdx', filename="legend.mdx",
                                 media_type='multipart/form-data')
        print(to_return)
        return to_return
    except Exception as e:
        print("Exception", e)
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_input"
)
async def get_task_input(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive task legend"""

    try:
        to_return = FileResponse(path=f'./data/problems/{_id}/input.mdx', filename="input.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_output"
)
async def get_task_output(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive task legend"""

    try:
        to_return = FileResponse(path=f'./data/problems/{_id}/output.mdx', filename="output.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_scoring"
)
async def get_problem_scoring(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive task legend"""

    try:
        to_return = FileResponse(path=f'./data/problems/{_id}/scoring.mdx', filename="scoring.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_notes"
)
async def get_notes(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())):
    """Retreive task legend"""

    try:
        to_return = FileResponse(path=f'./data/problems/{_id}/notes.mdx', filename="notes.mdx",
                                 media_type='multipart/form-data')
        return to_return
    except Exception:
        return get_error_response("FILE_NOT_FOUND")


@router.get(
    "/get_name"
)
async def get_name(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())) -> Any:
    """Retreive task name by task id"""

    task = await db.problem.get(_id)

    if task is None:
        return get_error_response("TASK_NOT_FOUND")

    return task.name
