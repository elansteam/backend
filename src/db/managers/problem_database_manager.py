"""ProblemDatabaseManager definition"""
from config import Config
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.helpers.auto_increment_database_interface import AutoIncrementDatabaseInterface
from db.models.problem import IntIdAnnotation
from db.models.problem import Problem
from db.models.annotations import NameAnnotation


class ProblemDatabaseManager(AbstractDatabaseManager, AutoIncrementDatabaseInterface):
    """Database methods to work with users"""

    collection_name = Config.Collections.problems

    async def get(self, problem: IntIdAnnotation) -> Problem | None:
        """
        Getting user by id
        Args:
            problem: the user id
        """

        task = await self.collection.find_one({"_id": problem})

        if task is None:
            return None
        return Problem(**task)

    async def insert_with_id(self, problem: Problem) -> int:
        """
        Insert used with auto increment
        Args:
            problem: used document to insert
        """
        return await self._insert_one_with_id(self.collection_name, problem)

    async def get_by_name(self, name: NameAnnotation) -> Problem | None:

        problem = await self.collection.find_one({"name": name})

        if problem is None:
            return None
        return Problem(**problem)
