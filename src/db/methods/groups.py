from pymongo.client_session import ClientSession

from db.types import types
from db.methods.helpers import insert_with_auto_increment_id
from .collections import groups


def get(group_id: int, session: ClientSession | None = None) -> types.Group | None:
    if (group := groups.find_one({"_id": group_id}, session=session)) is None:
        return None
    return types.Group(**group)


def insert(group: types.GroupWithoutID, session: ClientSession | None = None) -> int:
    return insert_with_auto_increment_id(groups, group.db_dump(), session)


def check_existence(group_id: int, session: ClientSession | None = None) -> bool:
    return groups.count_documents({"_id": group_id}, session=session) > 0


def add_member(group_id: int, member: types.Member, session: ClientSession | None = None) -> None:
    groups.update_one({"_id": group_id}, {"$push": {"members": member.model_dump()}}, session=session)


def is_user_in_group(user_id: int, group_id: int, session: ClientSession | None = None) -> bool:
    return groups.count_documents({"_id": group_id, "members": {"$elemMatch": {"id": user_id}}}, session=session) > 0
