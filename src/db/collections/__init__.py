"""All collections got by already configuring names."""

from db import db
from config import config

users = db.get_collection(config.database.collections.users)
domains = db.get_collection(config.database.collections.domains)
group_roles = db.get_collection(config.database.collections.group_roles)
groups = db.get_collection(config.database.collections.groups)
internal_counters = db.get_collection(config.database.collections.internal_counters)
roles = db.get_collection(config.database.collections.roles)
