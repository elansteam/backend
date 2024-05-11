"""
Module that allows work with database through implemented methods and models
also it provide annotations for specific types used in models and schemas
"""
import sys
from loguru import logger
from pymongo import MongoClient, database
from pymongo.errors import ServerSelectionTimeoutError
from config import config
from db.helpers import indexes_creation

# import submodules
from . import models
from . import schemas
from . import annotations
from . import methods
from . import collections

__all__ = ["models", "annotations", "methods", "schemas", "collections"]

# connection to database
logger.info("Connecting to database")

client: MongoClient = MongoClient(
    connect=config.database.connect_url.get_secret_value()
)

db: database.Database = client.get_database(config.database.name)

# trying check connection
try:
    client.server_info()
except ServerSelectionTimeoutError:
    logger.error("Database is not connected")
    sys.exit(1)

indexes_creation.create_indexes()

def close_connection():
    """Closing mongodb connection"""
    client.close()
