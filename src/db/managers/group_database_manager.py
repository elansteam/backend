"""GroupDatabaseManager definition"""
from src.db.helpers.abstract_database_manager import AbstractDatabaseManager
from src.db.models.group import Group
from src.config import Config
from src.db.helpers.AutoIncrementDatabaseInterface import AutoIncrementDatabaseInterface


class GroupDatabaseManager(AbstractDatabaseManager, AutoIncrementDatabaseInterface):
    """Database methods with groups"""

    collection_name = Config.Collections.groups

    async def get(self, _id: int) -> Group | None:
        """
        Getting group by id
        Args:
            _id: mongo object id
        Returns:
            Group object or None if not found
        """
        group = await self.collection.find_one({"_id": _id})
        if group is None:
            return None
        return Group(**group)

    async def insert_with_id(self, group: Group) -> None:
        """
        Insert used with auto increment
        Args:
            group: used document to insert
        """
        await self._insert_one_with_id(self.collection_name, group)
