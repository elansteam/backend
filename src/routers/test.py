"""Routers that can be accessed only in test mode"""

from fastapi import APIRouter
from loguru import logger

from utils.response import SuccessfulResponse
from config import config
from db import client


router = APIRouter()


@router.post("/cleanup", response_model=SuccessfulResponse[None])
async def cleanup():
    db = client.get_database(config.database.name)
    for collection_name in db.list_collection_names():
        db.get_collection(collection_name).delete_many({})
    logger.warning("CLEAR ALL COLLECTIONS")
    return
