"""
The set of database modles, that represents data, containing in Database
"""
from . import user
from . import group
from . import role
from . import entity

__all__ = ["user", "group", "role", "entity"]  # FIXME: it is not all modules
