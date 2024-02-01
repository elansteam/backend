"""Role database manager."""

from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.models.role import Role
from config import Config


class RoleDatabaseManager(AbstractDatabaseManager):
    """Role database manager."""

    collection_name = Config.Collections.roles

    async def insert(self, role: Role) -> None:
        """
        Insert new role to database
        Args:
            role: role to insert
        """
        await self.collection.insert_one(role.model_dump(by_alias=True))

    async def get(self, role_id: str) -> Role | None:
        """
        Get role by id
        Args:
            role_id: Target role id
        Returns:
            Role or None
        """
        result = await self.collection.find_one({"_id": role_id})
        if result is None:
            return None
        return Role(**result)
