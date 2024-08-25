"""Here collection and indexes are defined"""

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


users.create_index([("email", 1)], unique=True, name="email")
# domains.create_index([("target_id", 1)], unique=True, name="target_id")
