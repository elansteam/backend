from db.types import Role
from .collections import roles

def get(role_name: str) -> Role | None:
    roles.find_one({"_id": role_name})
