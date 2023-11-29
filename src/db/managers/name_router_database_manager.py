"""NameRouterDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.name_router import NameRouter
from config import Config
from bson.objectid import ObjectId


class NameRouterDatabaseManager(AbstractDatabaseManager):
    """Database methods to routing names"""

    collection_name = Config.Collections.name_router