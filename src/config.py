from base.singleton import Singleton


class Config(metaclass=Singleton):
    """Синглтон класс конфига всего сервиса"""

    db_path: str = "mongodb://localhost:27017"
    """Путь к базе данных"""

    db_max_pool_size: int = 10
    """Ограничение количества подключений"""

    db_name: str = "ELANDB"
    """Имя базы данных"""

    def __init__(self):
        """Возможна загрузка значений из файла"""
