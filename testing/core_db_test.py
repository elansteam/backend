"""File to test core database methods"""
import pytest
from config import Config
from db.mongo_manager import MongoManager
from database_fixtures import setup_and_teardown


@pytest.mark.asyncio
async def test_db_connection():
    """Checking connection to db"""
    await MongoManager.get_db().get_collection(Config.Collections.users).insert_one(
        {"test": "test"})

    num_documents = await MongoManager.get_db().get_collection(
        Config.Collections.users).count_documents(
        {"test": "test"}
    )

    assert num_documents == 1

    await MongoManager.get_db().get_collection(Config.Collections.users).insert_one(
        {"test": "test"})

    num_documents = await MongoManager.get_db().get_collection(
        Config.Collections.users).count_documents(
        {"test": "test"}
    )

    assert num_documents == 2
