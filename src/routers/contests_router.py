"""Groups endpoints"""
import tempfile
from typing import Any
from zipfile import ZipFile

from fastapi import APIRouter, Depends, UploadFile
from auth.utils import auth_user
from auth.permissions import Permissions, ALL_PERMISSIONS_ROLE_CODE
from utils.response_utils import get_error_response, get_response, get_response_model, \
    get_error_schema
from db.models.contest import Contest, ContestToCreate
from db.models.user import User
import db
from db.models.user import IntIdAnnotation

router = APIRouter()


@router.post(
    "/create",
    response_model=get_response_model(Contest),
    responses={
        400: get_error_schema("Failed to create contest")
    }
)
async def create_contest(contest_to_create: ContestToCreate,
                         _current_user: User = Depends(auth_user())) -> Any:
    """Creating new contest"""

    # check existing for all members

    linked_group = await db.group.get(contest_to_create.linked_group)

    if linked_group is None:
        return get_error_response("LINKED_GROUP_NOT_FOUND")

    if _current_user.id != linked_group.owner:
        return get_error_response("USER_NOT_GROUP_OWNER",
                                  status_code=401)  # TODO: make group permissions and roles

    if contest_to_create.domain is not None:
        status = await db.domain.reserve(contest_to_create.domain)
        if status is False:
            return get_error_response("DOMAIN_IN_USE")

    try:

        # result group
        contest = Contest(
            _id=1,  # not used
            name=contest_to_create.name,
            description=contest_to_create.description,
            domain=contest_to_create.domain,
            linked_group=contest_to_create.linked_group,
            tasks=[]
        )

        created_contest_id = await db.contest.insert_with_id(contest)

        await db.group.add_contest(contest.linked_group, created_contest_id)

        if contest.domain is not None:
            await db.domain.attach(contest.domain, "user", created_contest_id)

        created_contest = await db.contest.get(created_contest_id)

        return get_response(created_contest)

    except Exception as e:
        if contest_to_create.domain is not None:
            await db.domain.delete(
                contest_to_create.domain
            )  # if error occurs delete reserved entity
        raise e


@router.get(
    "/get",
    response_model=get_response_model(Contest),
    responses={
        400: get_error_schema("Failed to retrieve contest")
    }
)
async def get_contest(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())) -> Any:
    """Return a contest by id"""

    contest = await db.contest.get(_id)

    if contest is None:
        return get_error_schema("CONTEST_NOT_FOUND")

    return get_response(contest)


@router.post(
    "/add_task_by_zip"
)
async def add_task_by_zip(contest_id: IntIdAnnotation, task_archive: UploadFile):
    """Add a task to contest by zip"""

    with tempfile.NamedTemporaryFile() as file_object:
        # print(file_object.name)
        with open(file_object.name, "wb") as file_object1:
            file_object1.write(await task_archive.read())
        with ZipFile(file_object1.name, "r") as zip_file:
            with zip_file.open("css/tokens.css", "r") as theme_file:
                print(str(theme_file.read()))
