from abc import abstractmethod
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging
from src.config import Config
from src.base.singleton import Singleton


class AbstractDatabaseManager(metaclass=Singleton):
    """Абстрактный класс менеджера базы данных"""
    db: AsyncIOMotorDatabase
    client: AsyncIOMotorClient

    def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client[Config().db_name]
        logging.info("Connected to MongoDB.")

    def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")


