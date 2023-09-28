"""Взаимодействие с базой данных"""
import time
from typing import Any
import pymongo
from src.helpers import config
import pymongo.database


class Driver:
    """Интерфейс взаимодействия с MongoDb"""

    client: pymongo.MongoClient
    db: pymongo.database.Database

    @classmethod
    def init(cls):
        """Подключение базы данных"""
        cls.client = pymongo.MongoClient("localhost", 27017)
        cls.db = cls.client[config.DATA_BASE_NAME]

    @classmethod
    def get_temp(cls) -> dict:
        document = cls.db["Users"].find_one()
        return document

    # TODO: Добавить методы взаимодействия с БД
