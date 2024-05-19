"""Methods for interact with roles in database"""

from db.annotations import NameAnnotation
from db.models import Role


def get(role_name: NameAnnotation) -> Role | None:
    """Returns role by name"""
    return None  # FIXME
