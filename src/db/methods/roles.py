from pymongo.errors import DuplicateKeyError

from db import types
from .collections import roles


def get(role_id: str) -> types.role.Role | None:
    if (role := roles.find_one({"_id": role_id})) is None:
        return None
    return types.role.Role(**role)

def insert(role: types.role.Role) -> bool:
    try:
        roles.insert_one(role.model_dump())
    except DuplicateKeyError:
        return False
    return True
