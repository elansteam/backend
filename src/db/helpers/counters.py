"""Counters internal database manager for auto increment ids"""
from typing import Any, TypeVar
import db.helpers.abstract_database_manager
from config import Config
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel
from abc import abstractmethod

DatabaseManagerType = TypeVar("DatabaseManagerType",
                              bound=db.helpers.abstract_database_manager.AbstractDatabaseManager)


class AutoIncrementDatabaseInterface:
    """Internal database methods for auto increment ids"""

    __internal_collection_name: str = Config.Collections.internal_counters

    async def _insert_one_with_id(self,
                                  database_manager: DatabaseManagerType,
                                  document: BaseModel) -> Any:
        """
        Insert document to the collection with generated id
        Args:
            database_manager: the collection name
            document: the document to insert
        Returns:
            Result of `insert_one` method
        """

        internal_database_collection = database_manager.get_db().get_collection(
            self.__internal_collection_name
        )

        if internal_database_collection is None:
            raise ConnectionError("Database is not connected")

        while True:
            try:
                res = await internal_database_collection.find_one_and_update(
                    {"_id": database_manager.collection_name},
                    {"$inc": {"counter": 1}}, upsert=True, return_document=True
                )

                to_insert = document.model_dump(by_alias=True)
                to_insert["_id"] = res["counter"]

                return await database_manager.collection.insert_one(
                    to_insert
                )
            except DuplicateKeyError:
                continue

    @abstractmethod
    async def insert_with_id(self, document) -> None: ...
