"""
The set of schemas

A schema is an object representing data that is not in the database
It can be used to determine the response, aggregate properties, and so on.
"""
from . import user
from . import auth
from . import group
from . import contest
from . import submission

__all__ = [
    "user",
    "auth"
    "group",
    "contest",
    "submission",
]
