import tempfile
from typing import Any

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel

from auth.utils import auth_user
from utils.response_utils import get_error_response, get_response, get_response_model, \
    get_error_schema
from db.models.contest import Contest, ContestToCreate
from db.models.task import Task
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
    task_to_create = Task(
        _id=1,  # not used
        name=name
    )
    created_task_id = await db.task.insert_with_id(task_to_create)
    response = AddTask(created_task_id=created_task_id)
    return get_response(response)
