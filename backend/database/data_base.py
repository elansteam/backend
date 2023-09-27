"""Взаимодействие с базой данных"""
import pymongo
from backend import project_config
import pymongo.database


class DataBase:
    """Интерфейс взаимодействия с MongoDb"""

    client: pymongo.MongoClient
    db: pymongo.database.Database

    @classmethod
    def init(cls):
        """Подключение базы данных"""
        cls.client = pymongo.MongoClient("localhost", 27017)
        cls.db = cls.client[project_config.DATA_BASE_NAME]

    # TODO: Добавить методы взаимодействия с БД
