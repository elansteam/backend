"""UserDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
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
        await self.db.insert_one(**user.model_dump())

    async def get_by_name(self, user_name: str) -> User | None:
        """
        Getting user by username
        Args:
            user_name: username

        Returns:
            User object or None, if not found
        """

        user = await self.db.find_one({"name": user_name})
        if user is None:
            return None
        return User(**user)

    async def add_role(self, user_name: str, role_name: str) -> None:
        """
        Adding role to user
        Args:
            user_name: user where add
            role_name: role which add
        """

        await self.db.update_one({"name": user_name},
                                 {"$push": {"roles": role_name}})
