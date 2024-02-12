"""Global permissions enum"""
import enum

ALL_PERMISSIONS_ROLE_CODE: int = 2 ** 31 - 1
"""Number that contains all bits of permissions"""


class Permissions(enum.Enum):
    """Global Permissions enum"""
    # ADMIN = 0
    CREATE_GROUP = 1
    CREATE_ROLE = 2
    CHANGE_USER_ROLES = 3
    DELETE_USER = 4