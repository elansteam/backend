"""UserDatabaseManager definition"""
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.models.user import User
from config import Config


class UserDatabaseManager(AbstractDatabaseManager):
    """Database methods to work with users"""

    collection_name = Config.Collections.users

    async def create(self, user: User) -> None:
        """
        Creating user in database
        Args:
            user: user object to create
        """
        await self.collection.insert_one(**user.model_dump())

    async def get(self, user_id: int) -> User | None:
        """
        Getting user by id
        Args:
            user_id: the user id

        Returns:
            User object or None, if not found
        """

        user = await self.collection.find_one({"_id": user_id})
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
