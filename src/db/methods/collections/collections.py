"""
The module that receives all collections by the configured name and exports them
Moreover this module create indexes
"""
from pymongo.collection import Collection

from db.client import db
from config import config


roles: Collection = db.get_collection(config.database.collections.roles)
users: Collection = db.get_collection(config.database.collections.users)
groups: Collection = db.get_collection(config.database.collections.groups)
domains: Collection = db.get_collection(config.database.collections.domains)
contests: Collection = db.get_collection(config.database.collections.contests)
group_roles: Collection = db.get_collection(config.database.collections.group_roles)
group_members: Collection = db.get_collection(config.database.collections.group_members)
internal_counters: Collection = db.get_collection(config.database.collections.internal_counters)


# Indexes

# users
users.create_index(
    {"email": 1},
    partialFilterExpression={"email": {"$type": "string"}}
)

# contests
contests.create_index(
    {
        "group_id": 1,
        "local_domain": 1
    }
)
