from db.types.common import IntegerId
from db.types import User
from .collections import users


def get(user_id: IntegerId) -> User | None:
    user = users.find_one({
        "_id": user_id
    })
    if user is None:
        return None
    return User(**user)
