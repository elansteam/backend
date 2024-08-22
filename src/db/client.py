import sys
from pymongo import MongoClient, database
from pymongo.errors import ServerSelectionTimeoutError
from loguru import logger

from config import config


logger.info("Connecting to database")

client: MongoClient = MongoClient(config.database.connect_url.get_secret_value())

db: database.Database = client.get_database(config.database.name)

try:
    client.server_info()
except ServerSelectionTimeoutError:
    logger.error("Database is not connected (Timeout error)")
    sys.exit(1)

def close_connection():
    client.close()
