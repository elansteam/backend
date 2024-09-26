"""Here collection and indexes are defined"""

from typing import Any
from pymongo.collection import Collection
from db.client import db
from config import config


users = db.get_collection(config.database.collections.users)
organizations = db.get_collection(config.database.collections.organizations)
organization_members = db.get_collection(config.database.collections.organization_members)
internal_counters = db.get_collection(config.database.collections.internal_counters)


users.create_index([("email", 1)], unique=True)
organization_members.create_index([("target_id", 1), ("object_id", 1)], unique=True)
