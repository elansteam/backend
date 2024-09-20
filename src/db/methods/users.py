from pymongo.errors import DuplicateKeyError

from db.types import types
from .collections import users
from .helpers import insert_with_auto_increment_id


def get(user_id: int) -> types.User | None:
    if (user := users.find_one({"_id": user_id})) is None:
        return None
    return types.User(**user)


def get_by_email(email: str):
    if (user := users.find_one({"email": email})) is None:
        return None
    return types.User(**user)


def insert_user_with_id(user: types.UserWithoutID) -> int | None:
    """
    Returns:
        Inserted user id or None, if error occurred
    """
    try:
        return insert_with_auto_increment_id(users, user.db_dump())
    except DuplicateKeyError:
        return None
