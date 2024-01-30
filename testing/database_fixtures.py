"""
Main fixtures
"""
from loguru import logger
import pytest_asyncio
from motor.core import AgnosticDatabase

from src.config import Config
from src.db.MongoManager import MongoManager
import asyncio
import time


@pytest_asyncio.fixture(autouse=True)
async def setup_and_teardown():
    """Base fixture, that setting up database and start fastapi client"""

    # connection to database
    # AbstractDatabaseManager.connect_to_database(url=Config.db_connect_url)
    # Database.db = AbstractDatabaseManager.get_db()
    MongoManager.connect(Config.db_connect_url, Config.db_name)
    await MongoManager.get_client().drop_database(Config.db_name)

    yield

    # await asyncio.sleep(5)
    MongoManager.disconnect()
