from utils.singleton import Singleton
from enum import Enum


# TODO: add load values from env variables
class Config:
    """Синглтон класс конфига всего сервиса"""

    db_path: str = "mongodb://localhost:27017"
    """Путь к базе данных"""

    db_max_pool_size: int = 10
    """Ограничение количества подключений"""

    db_name: str = "ELANDB"
    """Имя базы данных"""

    class Collections:
        users = "Users"
        roles = "Roles"
        permissions = "Permissions"
        gpermissions = "GPermissions"
        groles = "GRoles"
        groups = "Groups"

    app_title = "ELAN api"
    """Заголовок приложения"""

    class Permissions:
        admin = "admin"
        """Высший тип права - позволено все"""

    class GPermissions:
        owner = "owner"
        """Высший тип права - позволено все"""

    @classmethod
    def init(cls):
        """Инициализация конфига из файлов"""
