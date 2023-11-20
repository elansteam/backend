"""Project config file"""
import os


class Config:
    """Синглтон класс конфига всего сервиса"""

    db_path: str = os.environ.get("DB_PATH")
    """Путь к базе данных"""

    db_name: str = os.environ.get("DB_NAME")
    """Имя базы данных"""

    class Collections:
        """Collection db names"""
        users = os.environ.get("COLLECTION_USERS")
        roles = os.environ.get("COLLECTION_ROLES")
        groles = os.environ.get("COLLECTION_GROLES")
        groups = os.environ.get("COLLECTION_GROUPS")

    class Auth:
        """Data for auth system"""
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
        ALGORITHM = os.environ.get("ALGORITHM")

        JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
        JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")

    app_title = os.environ.get("APP_TITLE")
    """Заголовок приложения"""
