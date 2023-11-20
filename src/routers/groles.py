"""Endpoints with group roles"""
from fastapi import APIRouter, Depends
from db.managers.grole_database_manager import GRoleDatabaseManager
from db.managers.group_database_manager import GroupDatabaseManager
from db.models.user import User
from src.auth.utils import auth_user, Permissions
from src.db.models.grole import GRole
from utils.utils import get_error_response, get_error_schema

router = APIRouter()

db_groles = GRoleDatabaseManager()
db_groups = GroupDatabaseManager()


@router.post(
    "/create",
    response_model=GRole,
    responses={
        400: get_error_schema("Failed to create grole"),
    }
)
async def create(grole: GRole,
                 _current_user: User = Depends(auth_user(
                     Permissions.C_CREATE_GROLE
                 ))):
    """Создание grole для группы"""

    if await db_groles.get_by_name(grole.name, grole.group) is not None:
        return get_error_response(
            f"GRole with name <{grole.name}> and group <{grole.group}> are exist yet")

    group = await db_groups.get_by_name(grole.group)

    if group is None:
        return get_error_response(f"Group with name <{grole.group}> isn`t exist")

    await db_groles.create(grole)

    await db_groups.add_grole(grole.group, grole.name)
    return grole
