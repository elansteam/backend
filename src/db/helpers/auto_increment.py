"""Implements method for insert object with autoincrement id"""

from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel
from config import config
from db import db

def insert_with_id(
    collection: str,
    document: BaseModel
) -> int:
    """Insert document with autoincrement id

    Args:
        collection: name of collection to insert
        document: document to insert

    Returns:
        int: id of inserted document
    """

    internal_database_collection = db.get_collection(
        config.database.collections.internal_counters
    )

    while True:
        try:
            res = internal_database_collection.find_one_and_update(
                {"_id": collection},
                {"$inc": {"counter": 1}}, upsert=True, return_document=True
            )

            to_insert = document.model_dump(by_alias=True)
            to_insert["_id"] = res["counter"]

            db.get_collection(collection).insert_one(
                to_insert
            )

            return res["counter"]
        except DuplicateKeyError:
            continue
