"""
The module that receives all collections by the configured name and exports them
Moreover this module create indexes
"""

from db.client import db
from config import config


roles = db.get_collection(config.database.collections.roles)
users = db.get_collection(config.database.collections.users)
groups = db.get_collection(config.database.collections.groups)
domains = db.get_collection(config.database.collections.domains)
contests = db.get_collection(config.database.collections.contests)
group_roles = db.get_collection(config.database.collections.group_roles)
group_members = db.get_collection(config.database.collections.group_members)
internal_counters = db.get_collection(config.database.collections.internal_counters)


users.create_index(
    {"email": 1},
    partialFilterExpression={"email": {"$type": "string"}}
)

contests.create_index(
    {
        "group_id": 1,
        "local_domain": 1
    }
)
