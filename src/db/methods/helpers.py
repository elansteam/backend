from typing import Any
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from db.types import types
from .collections import internal_counters, users, organizations, domains


def insert_with_auto_increment_id(
    collection: Collection[Any],
    document: dict[str, Any],
    session: ClientSession | None = None
) -> int:
    while True:
        try:
            result_id = internal_counters.find_one_and_update(
                {"_id": collection.name},
                {"$inc": {"counter": 1}}, upsert=True, return_document=True, session=session
            )["counter"]
            document["_id"] = result_id
            collection.insert_one(document, session=session)
            return result_id
        except DuplicateKeyError as e:
            if (
                e.details is None  or
                (key_pattern := e.details.get("keyPattern")) is None or
                key_pattern.get("_id") is None
            ):
                raise e

def get_related_collection(object_type: type[types.HasCollection]) -> Collection:
    match object_type:
        case types.User:
            return users
        case types.Organization:
            return organizations
        case types.Entity:
            return domains
    raise NotImplementedError("This type is not supported")
