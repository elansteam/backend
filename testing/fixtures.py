"""
Main fixtures
"""
import pytest
from config import Config
from db.abstract_database_manager import AbstractDatabaseManager


class DatabaseInterface(AbstractDatabaseManager):
    """
    Interface for getting db object from abstract database
    """
    def get_db(self):
        """
        Returns: directly returns database client
        """
        return self._db


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Base fixture, that setting up database and start fastapi client"""
    AbstractDatabaseManager.connect_to_database(url=Config.db_connect_url)

    _db = DatabaseInterface().get_db()  # TODO: add normal db connect
    client = AbstractDatabaseManager().client

    yield

    client.drop_database(Config.db_name)
    AbstractDatabaseManager.close_database_connection()
