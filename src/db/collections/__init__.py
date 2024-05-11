"""All collections got by already configuring names."""

from db import db as _db
from config import config as _config  # to improve type hints

users = _db.get_collection(_config.database.collections.users)
domains = _db.get_collection(_config.database.collections.domains)
group_roles = _db.get_collection(_config.database.collections.group_roles)
groups = _db.get_collection(_config.database.collections.groups)
internal_counters = _db.get_collection(_config.database.collections.internal_counters)
roles = _db.get_collection(_config.database.collections.roles)
group_members = _db.get_collection(_config.database.collections.group_members)
contests = _db.get_collection(_config.database.collections.contests)

__all__ = [
    "users",
    "domains",
    "group_roles",
    "internal_counters",
    "roles",
    "contests",
    "group_members"
]
