from typing import Any
from pymongo.errors import DuplicateKeyError

from db.types.user import User
from .collections import users
from .helpers import insert_with_auto_increment_id


def get(user_id: int) -> User | None:
    user = users.find_one({
        "_id": user_id
    })
    if user is None:
        return None
    return User(**user)

def get_by_email(email: str):
    user = users.find_one({
        "email": email
    })
    if user is None:
        return None
    return User(**user)

def insert_user_document_with_id(user_document: dict[str, Any]) -> int | None:
    """
    Returns: None if DuplicateKeyError. Else - inserted_user_id
    """
    try:
        return insert_with_auto_increment_id(
            users,
            user_document
        )
    except DuplicateKeyError:
        return None
