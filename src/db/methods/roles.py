from pymongo.errors import DuplicateKeyError
from db.types.role import Role
from .collections import roles

def get(role_name: str) -> Role | None:
    role = roles.find_one({"_id": role_name})

    if role is None:
        return None
    return Role(**role)

def insert(role: Role) -> bool:
    """
    Returns: False - if DuplicateKeyError, else - True
    """
    try:
        roles.insert_one(role.model_dump())
    except DuplicateKeyError:
        return False
    return True
