"""Groups endpoints"""
from typing import Any
from fastapi import APIRouter, Depends
from auth.utils import auth_user
from auth.permissions import Permissions, ALL_PERMISSIONS_ROLE_CODE
from utils.response_utils import get_error_response, get_response, get_response_model, \
    get_error_schema
from db.models.contest import Contest, ContestToCreate
from db.models.user import User
import db

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

        created_contest = await db.contest.get(created_contest_id)

        return get_response(created_contest)

    except Exception as e:
        if contest_to_create.domain is not None:
            await db.domain.delete(
                contest_to_create.domain
            )  # if error occurs delete reserved entity
        raise e