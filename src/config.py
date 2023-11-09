from src.base.singleton import Singleton
from enum import Enum


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
        in_group_permissions = "InGroupPermissions"
        in_group_roles = "InGroupRoles"
        groups = "Groups"

    app_title = "ELAN api"
    """Заголовок приложения"""

    class Permissions:
        admin = "admin"
        """Высший тип права - позволено все"""

    class InGroupPermissions:
        admin = "admin"
        """Высший тип права - позволено все"""

    @classmethod
    def init(cls):
        """Инициализация конфига из файлов"""
