"""File to test core database methods"""
import pytest
from config import Config
import pytest_asyncio
from testing.database_fixtures import setup_and_teardown
from db.helpers.abstract_database_manager import AbstractDatabaseManager
import db
from db.models.group import Group
from db.mongo_manager import MongoManager


@pytest.mark.asyncio
async def test_autoincrement_simple():
    """Testing autoincrement technology for group"""

    group_first = Group(
        name="first",
        owner=-1
    )

    group_second = Group(
        name="second",
        owner=-1
    )

    group_third = Group(
        name="third",
        owner=-1
    )

    collection = MongoManager.get_db().get_collection(Config.Collections.groups)

    await db.group.insert_with_id(group_first)

    assert await collection.count_documents({"name": "first"}) == 1

    temp_user = await collection.find_one({"name": "first"})

    assert temp_user["_id"] == 1

    await db.group.insert_with_id(group_second)

    assert await collection.count_documents({"name": "second"}) == 1

    assert await collection.count_documents({}) == 2

    temp_user = await collection.find_one({"name": "second"})

    assert temp_user["_id"] == 2

    # deleting first user

    await collection.delete_one({"name": "first"})

    assert await collection.count_documents({"name": "first"}) == 0

    await db.group.insert_with_id(group_third)

    assert await collection.count_documents({"name": "third"}) == 1

    temp_user = await collection.find_one({"name": "third"})

    assert temp_user["_id"] == 3


@pytest.mark.asyncio
async def test_autoincrement_stress():
    collection = MongoManager.get_db().get_collection(Config.Collections.groups)
    for i in range(100):
        current_user = Group(
            name=str(i + 1),
            owner=-1
        )

        await db.group.insert_with_id(current_user)

        temp_user = await collection.find_one({"name": str(i + 1)})

        assert temp_user["_id"] == i + 1
