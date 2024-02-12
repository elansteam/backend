"""UserDatabaseManager definition"""
from config import Config
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.helpers.auto_increment_database_interface import AutoIncrementDatabaseInterface
from db.models.task import IntIdAnnotation
from db.models.task import Task
from db.models.annotations import NameAnnotation


class TaskDatabaseManager(AbstractDatabaseManager, AutoIncrementDatabaseInterface):
    """Database methods to work with users"""

    collection_name = Config.Collections.tasks

    async def get(self, task_id: IntIdAnnotation) -> Task | None:
        """
        Getting user by id
        Args:
            task_id: the user id
        """

        task = await self.collection.find_one({"_id": task_id})

        if task is None:
            return None
        return Task(**task)

    async def insert_with_id(self, task: Task) -> int:
        """
        Insert used with auto increment
        Args:
            task: used document to insert
        """
        return await self._insert_one_with_id(self.collection_name, task)

    async def get_by_name(self, name: NameAnnotation) -> Task | None:

        task = await self.collection.find_one({"name": name})

        if task is None:
            return None
        return Task(**task)