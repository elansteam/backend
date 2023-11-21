"""AbstractDatabaseManager definition"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from motor.core import AgnosticCollection
from src.config import Config
from utils.singleton import Singleton


class AbstractDatabaseManager(Singleton):
    """Base class for database managers
    Usage:
    Make new database manager class and inherit of this class
    redefine collection_name, it should be representation of collection
    in database
    """
    _db: AsyncIOMotorDatabase = None
    _client: AsyncIOMotorClient = None

    collection_name = None

    @property
    def db(self) -> AgnosticCollection:
        """

        Returns: special collection by self.collection_name in MongoDB

        """
        return self._db[self.collection_name]

    @classmethod
    def connect_to_database(cls, url: str) -> None:
        """Method to connect to the database

        Args:
            url: MongoDB url
        """
        logging.info("Connecting to MongoDB.")
        cls._client = AsyncIOMotorClient(
            url,
            maxPoolSize=10,
            minPoolSize=10)
        cls._db = cls._client[Config().db_name]
        logging.info("Connected to MongoDB.")

    @classmethod
    def close_database_connection(cls) -> None:
        """
        Close connection to the database
        """
        logging.info("Closing connection with MongoDB.")
        cls._client.close()
        logging.info("Closed connection with MongoDB.")
