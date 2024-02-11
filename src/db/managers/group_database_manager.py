"""GroupDatabaseManager definition"""
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.models.group import Group
from config import Config
from db.helpers.auto_increment_database_interface import AutoIncrementDatabaseInterface
from db.models.annotations import IntIdAnnotation


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

    async def insert_with_id(self, group: Group) -> int:
        """
        Insert used with auto increment
        Args:
            group: used document to insert
        """
        return await self._insert_one_with_id(self.collection_name, group)

    async def get_all(self) -> list[Group]:
        to_return = []
        cursor = self.collection.find({})
        async for group in cursor:
            print(group)
            to_return.append(Group(**group))

        return to_return

    async def add_contest(self, group_id: IntIdAnnotation, contest_id: IntIdAnnotation) -> None:
        """
        Inserting new contest id in group contests
        Args:
            group_id: target group
            contest_id: contest to insert
        """
        await self.collection.update_one(
            {"_id": group_id},
            {"$push": {"contests": contest_id}}
        )
