"""File to test core database methods"""
import pytest
from config import Config
import pytest_asyncio
from testing.database_fixtures import Database, setup_and_teardown
from src.db.helpers.abstract_database_manager import AbstractDatabaseManager
from loguru import logger
import db


@pytest.mark.asyncio
async def test_db_connection():
    """Checking connection to db"""
    await Database.db.get_collection(Config.Collections.users).insert_one({"test": "test"})

    num_documents = await Database.db.get_collection(Config.Collections.users).count_documents(
        {"test": "test"}
    )

    assert num_documents == 1

    await Database.db.get_collection(Config.Collections.users).insert_one({"test": "test"})

    num_documents = await Database.db.get_collection(Config.Collections.users).count_documents(
        {"test": "test"}
    )

    assert num_documents == 2
