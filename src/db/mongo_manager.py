"""Core database mongo manager"""

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient
from pymongo.database import Database


class MongoManager:
    """The main class for communicate with database"""

    _db: Database | None = None
    _client: AgnosticClient | None = None

    @classmethod
    def get_db(cls) -> Database:
        """
        Get database
        Returns: database
        """

        if cls._db is None:
            logger.error("Database not initialized")
            raise ConnectionError("Database not initialized")

        return cls._db

    @classmethod
    def get_client(cls) -> AgnosticClient:
        """
        Get mongo client
        Returns: mongo client
        """

        if cls._client is None:
            logger.error("Client not initialized")
            raise ConnectionError("Client not initialized")

        return cls._client

    @classmethod
    def connect(cls, url: str, db_name: str) -> None:
        """
        Connect to database
        Args:
            url: path to database
            db_name: name for target database
        """
        cls._client = AsyncIOMotorClient(url)
        cls._db = cls._client.get_database(db_name)
        logger.info(f"Connecting to database: {db_name} by pass {url}")

        if cls._db is None:
            logger.error("Database is not connected")
            raise ConnectionError("Database is not connected")
        logger.info("Successfully connected to MongoDB.")

    @classmethod
    def disconnect(cls) -> None:
        """
        Disconnect from database
        """
        if cls._client is None:
            return
        logger.info("Closing connection with MongoDB.")
        cls._client.close()
        logger.info("Successfully closed connection with MongoDB.")
