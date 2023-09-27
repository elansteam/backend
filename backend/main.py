"""Основной файл"""
from backend.database.data_base import DataBase


def main():
    """Стартовая функция"""
    DataBase.init()  # подключение к БД


if __name__ == "__main__":
    main()
