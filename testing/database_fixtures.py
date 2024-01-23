"""
Main fixtures
"""
import pytest_asyncio
from config import Config
from db.helpers.abstract_database_manager import AbstractDatabaseManager


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_and_teardown():
    """Base fixture, that setting up database and start fastapi client"""

    # connection to database
    await AbstractDatabaseManager.connect_to_database(url=Config.db_connect_url)

    yield

    # await client.drop_database(Config.db_name)
    AbstractDatabaseManager.close_database_connection()
