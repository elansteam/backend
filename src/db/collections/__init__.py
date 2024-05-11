"""All collections got by already configuring names."""

from db import db
from config import config as _config  # to improve type hints

users = db.get_collection(_config.database.collections.users)
domains = db.get_collection(_config.database.collections.domains)
group_roles = db.get_collection(_config.database.collections.group_roles)
groups = db.get_collection(_config.database.collections.groups)
internal_counters = db.get_collection(_config.database.collections.internal_counters)
roles = db.get_collection(_config.database.collections.roles)

__all__ = [
    "users",
    "domains",
    "group_roles",
    "internal_counters",
    "roles"
]
