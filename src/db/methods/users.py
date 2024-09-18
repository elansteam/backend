from pymongo.errors import DuplicateKeyError
from pymongo.client_session import ClientSession

from db.types import types
from .collections import users
from .helpers import insert_with_auto_increment_id


def get(user_id: int, session: ClientSession | None = None) -> types.User | None:
    if (user := users.find_one({"_id": user_id}, session=session)) is None:
        return None
    return types.User(**user)


def get_by_email(email: str, session: ClientSession | None = None):
    if (user := users.find_one({"email": email}, session=session)) is None:
        return None
    return types.User(**user)


def insert_user(
    user: types.UserWithoutID, session: ClientSession | None = None
) -> int | None:
    """
    Returns:
        Inserted user id or None, if error occurred
    """
    try:
        return insert_with_auto_increment_id(users, user.db_dump(), session=session)
    except DuplicateKeyError:
        return None
