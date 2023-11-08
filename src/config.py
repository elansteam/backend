from src.base.singleton import Singleton


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

    app_title = "ELAN api"
    """Заголовок приложения"""

    @classmethod
    def init(cls):
        """Инициализация конфига из файлов"""
