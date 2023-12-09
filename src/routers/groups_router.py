"""Groups endpoints"""
from fastapi import APIRouter, Depends
from db.managers.group_database_manager import Group
from db.models.user import User
from db.models.group_role import GroupRole
from auth.utils import auth_user, Permissions
from utils.utils import get_error_response, get_error_schema
import db

router = APIRouter()


@router.post(
    "/create",
    response_model=Group,
    responses={
        400: get_error_schema("Failed to create group"),
    }
)
async def create(group: Group,
                 _current_user: User = Depends(auth_user(
                     Permissions.CAN_CREATE_GROUP
                 ))):
    """Group creating"""

    if await db.group.get_by_name(group.name) is not None:
        return get_error_response(f"Group with name <{group.name}> doesn't exist",
                                  400)

    if await db.user.get_by_name(group.owner) is None:
        return get_error_response(f"Owner with name <{group.owner}> doesn't exist",
                                  400)

    # FIXME
    # TODO вынести это в отдельное поле и сделать расширяемым
    await db.group_role.create(GroupRole.model_validate(
        {
            "name": "owner",
            "group": group.name,
            "gpermissions": ["owner"],
            "description": "The most powerful role in group"
        }
    ))

    await db.group_role.create(GroupRole.model_validate(
        {
            "name": "admin",
            "group": group.name,
            "group_permissions": ["admin"],
            "description": "Like owner but lower"  # FIXME
        }
    ))

    group.group_roles = []
    group.members = {}

    group.group_roles.append("owner")
    group.group_roles.append("admin")

    group.members[group.owner] = ["owner"]

    await db.group_role.create(group)
    return group


# TODO: add auth
@router.post(
    "/add_user",
    response_model=User,
    responses={
        400: get_error_schema("Failed add user to group"),
    }
)
async def add_user(user_name: str, group_name: str,
                   _current_user: User = Depends(auth_user(
                       Permissions.CAN_ADD_USER_TO_GROUP
                   ))):
    """Adding user to group"""

    raise NotImplementedError("Method not ready")
    # FIXME
    # group = await db_groups.get_by_name(group_name)
    #
    # # Проверка на существование группы
    # if group is None:
    #     return get_error_response(f"Group with name <{group_name}> isn`t exist")
    #
    # # аутентификация
    # group_members = await db_groups.get_members(group_name)
    #
    # if current_user.name not in group_members:
    #     return AUTH_FAILED
    #
    # # TODO: добавить адекватную проверку на права пока КОСТЫЛЬ
    #
    # if group.owner != current_user.name:
    #     return AUTH_FAILED
    #
    # # проверка валидности данных
    # user = await db_users.get_by_name(user_name)
    #
    # if user is None:
    #     return get_error_response(f"User with name <{user_name}> isn`t exist")
    #
    # await db_groups.add_user(group_name, user_name)
    #
    # return await db_users.get_by_name(user_name)
