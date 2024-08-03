from db.types import Role
from .collections import roles

def get(role_name: str) -> Role | None:
    role = roles.find_one({"_id": role_name})

    if role is None:
        return None
    return Role(**role)
