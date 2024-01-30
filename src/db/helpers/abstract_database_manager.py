"""AbstractDatabaseManager definition"""
from motor.core import AgnosticCollection, AgnosticClient
from src.utils.singleton import Singleton
from src.db.MongoManager import MongoManager


class AbstractDatabaseManager(Singleton):
    """Abstract DatabaseManager for inheritance"""

    collection_name: str | None = None

    @property
    def client(self) -> AgnosticClient:
        """
        Get MongoClient
        Returns: MongoClient instance
        """
        return MongoManager.get_client()

    @property
    def collection(self) -> AgnosticCollection:
        """
        Get MongoCollection for current collection name
        Returns: MongoCollection instance
        """
        if self.collection_name is None:
            raise NotImplementedError("collection name is not defined")

        return MongoManager.get_db().get_collection(self.collection_name)
