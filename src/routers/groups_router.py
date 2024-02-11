"""Groups endpoints"""
from typing import Any
from fastapi import APIRouter, Depends
from auth.utils import auth_user
from auth.permissions import Permissions, ALL_PERMISSIONS_ROLE_CODE
from utils.response_utils import get_error_response, get_response, get_response_model, \
    get_error_schema
from db.models.group import Group, GroupToCreate, GroupRole, GroupMember
from db.models.user import User
import db
from db.models.annotations import IntIdAnnotation

router = APIRouter()


@router.post(
    "/create",
    response_model=get_response_model(Group),
    responses={
        400: get_error_schema("Failed to create group")
    }
)
async def create_group(group_to_create: GroupToCreate,
                       _current_user: User = Depends(auth_user(
                           Permissions.CREATE_GROUP
                       ))) -> Any:
    """Creating new group"""

    # check existing for all members
    for member_id in group_to_create.members:
        member = await db.user.get(member_id)
        if member is None:
            return get_error_response("MEMBER_NOT_FOUND", data={
                "target_member_id": member_id
            })

    if group_to_create.domain is not None:
        status = await db.domain.reserve(group_to_create.domain)
        if status is False:
            return get_error_response("DOMAIN_IN_USE")

    try:
        members: list[GroupMember] = []

        # creating start group roles
        starter_roles: list[GroupRole] = [
            GroupRole(
                _id="admin",
                name="Admin",
                description="Admin",
                role_code=ALL_PERMISSIONS_ROLE_CODE
            )
        ]  # TODO: create here basic member role

        # generating members with roles
        for member_id in group_to_create.members:
            members.append(
                GroupMember(
                    _id=member_id,
                    permissions=0,  # TODO: add here basic member role
                    roles=[]
                )
            )

        # result group
        group = Group(
            _id=1,  # not used
            owner=_current_user.id,
            name=group_to_create.name,
            description=group_to_create.description,
            domain=group_to_create.domain,
            members=members,
            roles=starter_roles
        )

        created_group_id = await db.group.insert_with_id(group)

        created_group = await db.group.get(created_group_id)

        return get_response(created_group)

    except Exception as e:
        if group_to_create.domain is not None:
            await db.domain.delete(group_to_create.domain)  # if error occurs delete reserved entity
        raise e


@router.get(
    "/get",
    response_model=Group,
    responses={
        400: get_error_schema("Failed to retreive group")
    }
)
async def get_group(_id: IntIdAnnotation, _current_user: User = Depends(auth_user())) -> Any:
    """Retreive group by id"""

    group = await db.group.get(_id)

    if group is None:
        return get_error_response("GROUP_NOT_FOUND")

    return get_response(group)
