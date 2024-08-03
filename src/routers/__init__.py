"""Module to manage routers"""

from . import auth
from . import users
from . import roles
from . import groups
from . import tests
from . import problems
from . import contests
from . import submissions


__all__ = [
    "auth",
    "users",
    "roles",
    "groups",
    "tests",
    "problems",
    "contests",
    "submissions"
]
