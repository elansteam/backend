"""All collections got by already configuring names. And create mongo indexes"""

from db import db as _db
from config import config as _config  # to improve type hints

roles = _db.get_collection(_config.database.collections.roles)
users = _db.get_collection(_config.database.collections.users)
groups = _db.get_collection(_config.database.collections.groups)
domains = _db.get_collection(_config.database.collections.domains)
contests = _db.get_collection(_config.database.collections.contests)
group_roles = _db.get_collection(_config.database.collections.group_roles)
group_members = _db.get_collection(_config.database.collections.group_members)
internal_counters = _db.get_collection(_config.database.collections.internal_counters)

__all__ = [
    "users",
    "roles",
    "domains",
    "contests",
    "group_roles",
    "group_members",
    "internal_counters"
]


# Creating mongo indexes

# users
users.create_index(
    {"email": 1},
    partialFilterExpression={"email": {"$ne": None}}
)
# contests
contests.create_index(
    {
        "group_id": 1,
        "local_domain": 1
    }
)
