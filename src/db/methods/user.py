"""Methods for interact with users in database"""

from db.annotations import IntIdAnnotation
from db.models import User


def get(user_id: IntIdAnnotation) -> User | None:    
    """Returns user by id"""
    return None  # FIXME
