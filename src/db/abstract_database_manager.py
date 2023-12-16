"""AbstractDatabaseManager definition"""
import logging
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
    _client: AgnosticClient | None = None
    collection_name: str = ""
    """Child class collection name"""

    @property
    def db(self) -> AgnosticCollection:
        """

        Returns: special collection by self.collection_name in MongoDB

        """
        if self._db is None:
            raise ConnectionError("Database is not connected")
        return self._db[self.collection_name]

    @property
    def client(self) -> AgnosticClient:
        """

        Returns: special database client

        """
        return self.client

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
        cls._db = cls._client[Config.db_name]
        logging.info("Connected to MongoDB.")

    @classmethod
    def close_database_connection(cls) -> None:
        """
        Close connection to the database
        """
        if cls._client is None:
            return
        logging.info("Closing connection with MongoDB.")
        cls._client.close()
        logging.info("Closed connection with MongoDB.")
