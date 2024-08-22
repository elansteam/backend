"""Global Permissions"""
from enum import Enum

ALL_PERMISSIONS_ROLE_CODE: int = 2 ** 63 - 1


class Permissions(Enum):
    CREATE_GROUP = 1
    CREATE_ROLE = 2
    CHANGE_USER_ROLES = 3
    DELETE_USER = 4
