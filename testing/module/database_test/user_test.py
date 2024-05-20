"""File to test core database methods"""
import pytest
from config import Config
import pytest_asyncio
from testing.database_fixtures import setup_and_teardown
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from loguru import logger
import db as db
from db.models.user import User
from db.mongo_manager import MongoManager


@pytest.mark.asyncio
async def test_autoincrement_simple():
    """Testing autoincrement technology for user"""

    user_first = User(
        _id=1,  # not used
        first_name="first",
        last_name="user",
        email="test@gmail.com",
        password_hash="test_hash"
    )

    user_second = User(
        _id=1,  # not used
        first_name="second",
        last_name="user",
        email="test@gmail.com",
        password_hash="test_hash"
    )

    user_third = User(
        _id=1,  # not used
        first_name="third",
        last_name="user",
        email="test@gmail.com",
        password_hash="test_hash"
    )

    logger.info("Created all users")

    collection = MongoManager.get_db().get_collection(Config.Collections.users)

    await db.user.insert_with_id(user_first)

    assert await collection.count_documents({"first_name": "first"}) == 1
    logger.info("First user added to database")

    temp_user = await collection.find_one({"first_name": "first"})

    assert temp_user["_id"] == 1
    logger.info("Firstly added user has id = 1")

    await db.user.insert_with_id(user_second)

    assert await collection.count_documents({"first_name": "second"}) == 1
    logger.info("Second user added to database")

    assert await collection.count_documents({}) == 2

    temp_user = await collection.find_one({"first_name": "second"})

    assert temp_user["_id"] == 2
    logger.info("Secondly added user has id = 2")

    # deleting first user

    await collection.delete_one({"first_name": "first"})

    assert await collection.count_documents({"first_name": "first"}) == 0

    await db.user.insert_with_id(user_third)

    assert await collection.count_documents({"first_name": "third"}) == 1

    temp_user = await collection.find_one({"first_name": "third"})

    assert temp_user["_id"] == 3


@pytest.mark.asyncio
async def test_autoincrement_stress():
    collection = MongoManager.get_db().get_collection(Config.Collections.users)

    for i in range(100):
        current_user = User(
            _id=1,  # not used
            first_name=str(i + 1),
            last_name="user",
            email="test@gmail.com",
            password_hash="test_hash"
        )
        await db.user.insert_with_id(current_user)

        temp_user = await collection.find_one({"first_name": str(i + 1)})

        assert temp_user["_id"] == i + 1
