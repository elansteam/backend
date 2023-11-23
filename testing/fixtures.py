"""
Main fixtures
"""
import os
import pytest
from src.config import Config
from src.db.abstract_database_manager import AbstractDatabaseManager
from src.db.managers.role_database_manager import RoleDatabaseManager
from src.db.managers.user_database_manager import UserDatabaseManager
from src.db.managers.group_database_manager import GroupDatabaseManager
from src.db.managers.grole_database_manager import GRoleDatabaseManager


class DatabaseInterface(AbstractDatabaseManager):

    def get_db(self):
        """
        Returns: directly returns database client
        """
        return self._db


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Base fixture, that setting up database and start fastapi client"""
    AbstractDatabaseManager.connect_to_database(url=Config.db_path)

    db = DatabaseInterface().get_db()
    client = AbstractDatabaseManager().client

    yield

    client.drop_database(Config.db_name)
    AbstractDatabaseManager.close_database_connection()
