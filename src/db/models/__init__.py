"""
The set of database modles, that represents data, containing in Database
"""
from . import user
from . import group
from . import role
from . import entity
from . import contest
from . import problem
from . import submission

__all__ = [
    "user",
    "group",
    "role",
    "entity",
    "contest",
    "submission",
    "problem",
]
