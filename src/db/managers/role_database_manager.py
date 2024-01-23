"""Roles database manager definition"""
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.models.role import Role
from config import Config


class RoleDatabaseManager(AbstractDatabaseManager):
    """Role database methods"""

    collection_name = Config.Collections.roles

    async def get(self, role_id: str) -> Role | None:
        """Get role by ID

        Args:
            role_id (str): the role

        Returns:
            role object or None if not found
        """
        role = await self.collection.find_one({"_id": role_id})

        if role is None:
            return None

        return Role(**role)


    async def create(self, role: Role) -> None:
        """Insert new role to the database

        Args:
            role: the role to insert
        """
        await self.collection.insert_one(role.model_dump())
