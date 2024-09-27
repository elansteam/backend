from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError


from t import types
from .helpers import insert_with_auto_increment_id
from .collections import users


def get_user(user_id: int, s: ClientSession | None = None) -> types.User | None:
    if (user := users.find_one({"_id": user_id}, session=s)) is None:
        return None
    return types.User(**user)


def get_user_by_email(email: str, s: ClientSession | None = None):
    if (user := users.find_one({"email": email}, session=s)) is None:
        return None
    return types.User(**user)


def insert_user(user: types.UserWithoutID, s: ClientSession | None = None) -> int | None:
    try:
        return insert_with_auto_increment_id(users, user.db_dump(), session=s)
    except DuplicateKeyError:
        return None


def check_user_existence(user_id: int, s: ClientSession | None = None) -> bool:
    return users.count_documents({"_id": user_id}, session=s) > 0
