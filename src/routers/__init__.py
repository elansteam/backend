"""Module to manage routers"""
from . import users_router
from . import roles_router
from . import groups_router
# from . import domain_router
__all__ = ["users_router", "roles_router", "groups_router"]
