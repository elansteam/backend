"""Взаимодействие с базой данных"""
import time
from typing import Any
import pymongo
import src.settings
import pymongo.database
from src.database.collections.user import User


class Driver:
    """Интерфейс взаимодействия с MongoDb"""

    client: pymongo.MongoClient
    db: pymongo.database.Database

    @classmethod
    def __call__(cls):
        return cls.db

    @classmethod
    def init(cls):
        """Подключение базы данных"""
        cls.client = pymongo.MongoClient("localhost", 27017)
        cls.db = cls.client[src.settings.DATA_BASE_NAME]

    # @classmethod
    # def get_temp(cls) -> User:
    #     """Возвращает некоторый объект User"""
    #     document = cls.db["Users"].find_one()
    #     return User.model_construct(document)

    # TODO: Добавить методы взаимодействия с БД
