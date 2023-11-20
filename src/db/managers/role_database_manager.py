"""Roles database manager"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.role import Role
from config import Config


class RoleDatabaseManager(AbstractDatabaseManager):
    """Role database manager"""

    collection_name = Config.Collections.roles

    async def get_by_name(self, name: str) -> Role | None:
        """Get role by name

        Args:
            name (str): the role name

        Returns:
            Role | None: role object or None
        """
        role = await self.db.find_one({"name": name})

        if role is None:
            return None

        return Role(**role)

    async def create(self, role: Role) -> None:
        """Insert new role to the database

        Args:
            role (Role): the role to insert
        """
        await self.db.insert_one({**role.model_dump()})
