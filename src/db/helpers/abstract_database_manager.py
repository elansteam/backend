"""AbstractDatabaseManager definition"""
from loguru import logger
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection, AgnosticDatabase, AgnosticClient
from config import Config
from utils.singleton import Singleton


class AbstractDatabaseManager(Singleton):
    """Base class for database managers
    Usage:
    Make new database manager class and inherit of this class
    redefine collection_name, it should be representation of collection
    in database
    """
    _db: AgnosticDatabase | None = None
    client: AgnosticClient | None = None
    collection_name: str = ""
    """Child class collection name"""

    @property
    def collection(self) -> AgnosticCollection:
        """
        Returns: special collection by self.collection_name in MongoDB
        """
        if self._db is None:
            raise ConnectionError("Database is not connected")
        return self._db[self.collection_name]

    @classmethod
    def connect_to_database(cls, url: str) -> None:
        """Method to connect to the database
        Args:
            url: MongoDB url
        """

        # Create a new client and connect to the server
        cls.client = AsyncIOMotorClient(url)
        cls._db = cls.client[Config.db_name]
        logger.info("Successfully connected to MongoDB.")

    @classmethod
    def close_database_connection(cls) -> None:
        """
        Close connection to the database
        """
        if cls.client is None:
            return
        logger.info("Closing connection with MongoDB.")
        cls.client.close()
        logger.info("Successfully closed connection with MongoDB.")

    @classmethod
    def get_db(cls) -> AgnosticDatabase | None:
        """
        Returns: database object
        """
        return cls._db
