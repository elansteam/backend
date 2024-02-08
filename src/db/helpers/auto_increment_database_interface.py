"""Counters internal database manager for auto increment ids"""
from config import Config
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel
from abc import abstractmethod
from db.mongo_manager import MongoManager
from loguru import logger
from typing import TypeVar, Any

ChildOfBaseModel = TypeVar("ChildOfBaseModel", bound=BaseModel)


class AutoIncrementDatabaseInterface:
    """Internal database methods for auto increment ids"""

    __internal_collection_name: str = Config.Collections.internal_counters

    async def _insert_one_with_id(
        self, target_collection: str, document: BaseModel
    ) -> int:
        """
        Insert document to the collection with generated id
        Args:
            target_collection: target collection name
            document: the document to insert
        Returns:
            id for new created element
        """

        internal_database_collection = MongoManager.get_db().get_collection(
            self.__internal_collection_name
        )

        if internal_database_collection is None:
            raise ConnectionError("Database is not connected")

        while True:
            try:
                res = await internal_database_collection.find_one_and_update(
                    {"_id": target_collection}, {"$inc": {
                        "counter": 1
                    }},
                    upsert=True,
                    return_document=True
                )

                to_insert = document.model_dump(by_alias=True)
                to_insert["_id"] = res["counter"]

                await MongoManager.get_db(
                ).get_collection(target_collection).insert_one(to_insert)
                if not isinstance(res["counter"], int):
                    logger.error(
                        f"Database returned incorrect counter: {res['counter']}"
                    )
                    raise ValueError("Incorrect type for database response")
                return res["counter"]
            except DuplicateKeyError:
                continue

    @abstractmethod
    async def insert_with_id(self, document: Any) -> int:
        raise NotImplementedError
