"""Methods for interact with users in database"""
from loguru import logger

from db.client import db
from . import collections


def test():
    """Test method"""

    logger.info(db)
    logger.info(collections.users)
    logger.info(collections.internal_counters)
