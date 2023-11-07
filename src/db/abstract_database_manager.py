from abc import abstractmethod
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging
from src.config import Config
from src.base.singleton import Singleton


class AbstractDatabaseManager(Singleton):
    """Абстрактный класс менеджера базы данных"""
    _db: AsyncIOMotorDatabase
    _client: AsyncIOMotorClient

    collection_name = None

    @property
    def db(self):
        return self._db[self.collection_name]

    @classmethod
    def connect_to_database(cls, path: str):
        logging.info("Connecting to MongoDB.")
        cls._client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        cls._db = cls._client[Config().db_name]
        logging.info("Connected to MongoDB.")

    @classmethod
    def close_database_connection(cls):
        logging.info("Closing connection with MongoDB.")
        cls._client.close()
        logging.info("Closed connection with MongoDB.")
