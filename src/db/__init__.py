"""
Module that allows work with database through implemented methods and models
also it provide annotations for specific types used in models and schemas
"""
import sys
from loguru import logger
from pymongo import MongoClient, database
from pymongo.errors import ServerSelectionTimeoutError
from config import config

__all__ = [
    "models",
    "annotations",
    "methods",
    "schemas",
    "collections"
]

# connection to database
logger.info("Connecting to database")

client: MongoClient = MongoClient(config.database.connect_url.get_secret_value())

db: database.Database = client.get_database(config.database.name)

# checking connection
try:
    client.server_info()
except ServerSelectionTimeoutError:
    logger.error("Database is not connected (Timeout error)")
    sys.exit(1)

def close_connection():
    """Closing mongodb connection"""
    client.close()
