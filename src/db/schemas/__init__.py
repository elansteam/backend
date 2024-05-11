"""
The set of schemas

A schema is an object representing data that is not in the database
It can be used to determine the response, aggregate properties, and so on.
"""
from . import user
from . import contest
from . import group
from . import submission

__all__ = [
    "user",
    "group",
    "contest",
    "submission",
]
