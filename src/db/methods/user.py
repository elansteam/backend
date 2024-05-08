"""Methods for interact with users in database"""
from db import db
from loguru import logger

def test():
    """Test method function"""
    logger.info("test")
    logger.info(db)
    