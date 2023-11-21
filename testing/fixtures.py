"""
Main fixtures
"""
from src.config import Config
import os
from src.db.abstract_database_manager import AbstractDatabaseManager
import pytest


class DatabaseInterface(AbstractDatabaseManager):

    def get_db(self):
        """
        Returns: directly returns database client
        """
        return self._db


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Base fixture, that setting up database and start fastapi client"""
    AbstractDatabaseManager.connect_to_database(Config.db_path)
    yield
    AbstractDatabaseManager.close_database_connection()
