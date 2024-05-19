"""Methods for interact with users in database"""

from db.annotations import IntIdAnnotation
from db.models import User
from .collections import users


def get(user_id: IntIdAnnotation) -> User | None:
    """Returns user by id"""
    user = users.find_one({
        "_id": user_id
    })
    if user is None:
        return None
    return User(**user)
