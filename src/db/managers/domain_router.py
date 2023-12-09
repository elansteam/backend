"""Domain router definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.domain_router import DomainRouter
from config import Config
from bson.objectid import ObjectId


class DomainRouter(AbstractDatabaseManager):
    """Routing and manage object namas"""

    collection_name = Config.Collections.domain_router
    