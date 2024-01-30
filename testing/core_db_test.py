"""File to test core database methods"""
import pytest
from src.config import Config
import pytest_asyncio
from database_fixtures import setup_and_teardown
from src.db.helpers.abstract_database_manager import AbstractDatabaseManager
from loguru import logger
import src.db
from src.db.MongoManager import MongoManager


@pytest.mark.asyncio
async def test_db_connection():
    """Checking connection to db"""
    await MongoManager.get_db().get_collection(Config.Collections.users).insert_one({"test": "test"})

    num_documents = await MongoManager.get_db().get_collection(Config.Collections.users).count_documents(
        {"test": "test"}
    )

    assert num_documents == 1

    await MongoManager.get_db().get_collection(Config.Collections.users).insert_one({"test": "test"})

    num_documents = await MongoManager.get_db().get_collection(Config.Collections.users).count_documents(
        {"test": "test"}
    )

    assert num_documents == 2
