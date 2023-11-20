"""Database manager class"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from motor.core import AgnosticCollection
from src.config import Config
from utils.singleton import Singleton


class AbstractDatabaseManager(Singleton):
    """Abstract database manager"""
    _db: AsyncIOMotorDatabase
    _client: AsyncIOMotorClient

    collection_name = None

    @property
    def db(self) -> AgnosticCollection:
        """Property, which returns special collection for child class"""
        return self._db[self.collection_name]

    @classmethod
    def connect_to_database(cls, url: str):
        """Method to connect to the database

        Args:
            url (str): MongoDB url
        """
        logging.info("Connecting to MongoDB.")
        cls._client = AsyncIOMotorClient(
            url,
            maxPoolSize=10,
            minPoolSize=10)
        cls._db = cls._client[Config().db_name]
        logging.info("Connected to MongoDB.")

    @classmethod
    def close_database_connection(cls):
        """Close connection to the database"""
        logging.info("Closing connection with MongoDB.")
        cls._client.close()
        logging.info("Closed connection with MongoDB.")
