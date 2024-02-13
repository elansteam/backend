"""SubmissionatabaseManager definition"""
from config import Config
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.helpers.auto_increment_database_interface import AutoIncrementDatabaseInterface
from db.models.problem import IntIdAnnotation
from db.models.submission import Submission


class SubmissionDatabaseManager(AbstractDatabaseManager, AutoIncrementDatabaseInterface):
    """Database manager to work with submissions"""

    collection_name = Config.Collections.submissions

    async def get(self, submission_id: IntIdAnnotation) -> Submission | None:
        """
        Getting submission by id
        Args:
            submission_id: the submission id
        """

        submission = await self.collection.find_one({"_id": submission_id})

        if submission is None:
            return None
        return Submission(**submission)

    async def insert_with_id(self, submission: Submission) -> int:
        """
        Insert submission with auto increment
        Args:
            submission: submission document to insert
        """
        return await self._insert_one_with_id(self.collection_name, submission)

    async def attach_solution_path(
            self,
            submission_id: IntIdAnnotation,
            solution_path: str
    ) -> None:
        """
        Attaching source code to submission
        Args:
            submission_id: submission id
            solution_path: the source code path
        """

        await self.collection.update_one({"_id": submission_id}, {"$set": {
            "solution_path": solution_path
        }})
