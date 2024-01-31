"""UserDatabaseManager definition"""
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.helpers.auto_increment_database_interface import AutoIncrementDatabaseInterface
from db.models.user import User
from config import Config
from loguru import logger


class UserDatabaseManager(AbstractDatabaseManager, AutoIncrementDatabaseInterface):
    """Database methods to work with users"""

    collection_name = Config.Collections.users

    async def get(self, user_id: int) -> User | None:
        """
        Getting user by id
        Args:
            user_id: the user id

        Returns:
            User object or None, if not found
        """

        user = await self.collection.find_one({"_id": user_id})
        logger.debug(f"User with id {user_id} found as {user}")
        if user is None:
            return None
        return User(**user)

    async def get_by_email(self, email: str) -> User | None:
        """
        Getting user by email
        Args:
            email: the email

        Returns:
            User object or None, if not found
        """

        user = await self.collection.find_one({"email": email})
        if user is None:
            return None
        return User(**user)

    async def add_role(self, user_id: int, role_id: str) -> None:
        """
        Adding role to user
        Args:
            user_id: the user
            role_id: the role
        """

        await self.collection.update_one(
            {"_id": user_id},
            {"$push": {"roles": role_id}}
        )

    async def delete_role(self, user_id: int, role_id: str) -> None:
        """
        Deleting role to user
        Args:
            user_id: target user
            role_id: role to delete
        """
        await self.collection.update_one(
            {"_id": user_id},
            {"$pull": {"roles": role_id}}
        )

    async def insert_with_id(self, user: User) -> int:
        """
        Insert used with auto increment
        Args:
            user: used document to insert
        """
        return await self._insert_one_with_id(self.collection_name, user)
