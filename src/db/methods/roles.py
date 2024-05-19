"""Methods for interact with roles in database"""

from db.annotations import NameAnnotation
from db.models import Role
from .collections import roles


def get(role_name: NameAnnotation) -> Role | None:
    """Returns role by name"""
    role = roles.find_one(role_name)
    if role is None:
        return None
    return Role(**role)
