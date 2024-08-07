from pymongo.errors import DuplicateKeyError

from db.types.user import User
from .collections import users
from .helpers import insert_with_auto_increment_id


def get(user_id: int) -> User | None:
    if (user := users.find_one({"_id": user_id})) is None:
        return None
    return User(**user)

def get_by_email(email: str):
    if (user := users.find_one({"email": email})) is None:
        return None
    return User(**user)

def insert_user_with_id(
    email: str,
    hashed_password: str,
    roles: list[str] | None = None
) -> int | None:
    """
    Returns:
        Inserted user id or None, if error occurred
    """
    try:
        return insert_with_auto_increment_id(
            users,
            {
                "email": email,
                "hashed_password": hashed_password,
                "roles": roles or []
            }
        )
    except DuplicateKeyError:
        return None
