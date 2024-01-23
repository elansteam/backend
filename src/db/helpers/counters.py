"""Counters internal database manager for auto increment ids"""
from typing import Any, TypeVar
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from config import Config
from pymongo.errors import DuplicateKeyError

DatabaseManagerType = TypeVar("DatabaseManagerType", bound=AbstractDatabaseManager)

class InternalCountersDatabaseManager(AbstractDatabaseManager):
    """Internal database methods for auto increment ids"""

    __internal_collection_name: str = Config.Collections.internal_counters

    async def _insert_one_with_id(self, collection: DatabaseManagerType, document: Any) -> Any:
        """
        Insert document to the collection with generated id
        Args:
            collection_name: the collection name
            document: the document to insert
        Returns:
            Result of `insert_one` method
        """
        while True:
            try:
                if (self._db is None):
                    raise ConnectionError("Database is not connected")
                
                res = await self._db.get_collection(self.__internal_collection_name).find_one_and_update({"_id": collection.collection_name}, {"$inc": {"counter": 1}}, upsert=True, return_document=True)
                return await collection.db.insert_one({"_id": res["counter"], **document})
            except DuplicateKeyError:
                continue
