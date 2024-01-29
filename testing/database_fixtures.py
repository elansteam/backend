"""
Main fixtures
"""
from loguru import logger
import pytest_asyncio
from motor.core import AgnosticDatabase

from config import Config
from db.helpers.abstract_database_manager import AbstractDatabaseManager
import asyncio
import time

class Database:
    db: AgnosticDatabase | None = None


@pytest_asyncio.fixture(autouse=True)
async def setup_and_teardown():
    """Base fixture, that setting up database and start fastapi client"""

    # connection to database
    AbstractDatabaseManager.connect_to_database(url=Config.db_connect_url)
    await AbstractDatabaseManager.client.drop_database(Config.db_name)
    Database.db = AbstractDatabaseManager.get_db()



    yield


    # await asyncio.sleep(5)
    AbstractDatabaseManager.close_database_connection()
    logger.info("Dropped database and closed connection")
