"""NameRouterDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from config import Config


class NameRouterDatabaseManager(AbstractDatabaseManager):
    """Database methods to routing names"""

    collection_name = Config.Collections.name_router