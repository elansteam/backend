from typing import Any
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from .collections import internal_counters


def insert_with_auto_increment_id(
    collection: Collection[Any],
    document: dict[str, Any]
) -> int:
    while True:
        try:
            result_id = internal_counters.find_one_and_update(
                {"_id": collection.name},
                {"$inc": {"counter": 1}}, upsert=True, return_document=True
            )["counter"]
            document["_id"] = result_id
            collection.insert_one(document)
            return result_id
        except DuplicateKeyError as e:
            if (
                e.details is None  or
                (key_pattern := e.details.get("keyPattern")) is None or
                key_pattern.get("_id") is None
            ):
                raise e
