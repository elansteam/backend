"""Contest database manager definition"""
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.models.contest import Contest
from config import Config
from db.helpers.auto_increment_database_interface import AutoIncrementDatabaseInterface


class ContestDatabaseManager(AbstractDatabaseManager, AutoIncrementDatabaseInterface):
    """Database methods with contest"""

    collection_name = Config.Collections.contests

    async def get(self, _id: int) -> Contest | None:
        """
        Getting contest by id
        Args:
            _id: mongo object id
        Returns:
            Group object or None if not found
        """
        contest = await self.collection.find_one({"_id": _id})
        if contest is None:
            return None
        return Contest(**contest)

    async def insert_with_id(self, contest: Contest) -> int:
        """
        Insert used with auto increment
        Args:
            contest: used document to insert
        """
        return await self._insert_one_with_id(self.collection_name, contest)

    async def get_all(self) -> list[Contest]:
        """
        Returns: returning all contest objects
        """
        to_return = []
        cursor = self.collection.find({})
        async for group in cursor:
            to_return.append(Contest(**group))

        return to_return
