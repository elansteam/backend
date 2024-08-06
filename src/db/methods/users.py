from pymongo.errors import DuplicateKeyError

from typing import Any
from db.types.common import IntegerId, Email
from db.types.user import User
from .collections import users
from .helpers import insert_with_auto_increment_id


def get(user_id: IntegerId, session=None) -> User | None:
    user = users.find_one({
        "_id": user_id
    }, session=session)
    if user is None:
        return None
    return User(**user)

def get_by_email(email: Email, session=None):
    user = users.find_one({
        "email": email
    }, session=session)
    if user is None:
        return None
    return User(**user)

def insert_user_document(user_document: dict[str, Any]) -> IntegerId | None:
    try:
        return insert_with_auto_increment_id(
            users,
            user_document
        )
    except DuplicateKeyError:
        return None
