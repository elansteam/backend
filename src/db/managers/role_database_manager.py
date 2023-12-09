"""Roles database manager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.role import Role
from config import Config
from bson.objectid import ObjectId


class RoleDatabaseManager(AbstractDatabaseManager):
    """Role database methods"""

    collection_name = Config.Collections.roles

    async def get_by_name(self, role_name: str) -> Role | None:
        """Get role by name

        Args:
            role_name (str): the role name

        Returns:
            role object or None if not found
        """
        role = await self.db.find_one({"name": role_name})

        if role is None:
            return None

        return Role(**role)

    async def get_by_id(self, _id: ObjectId) -> Role | None:
        """
        Getting role by id
        Args:
            _id: mongo object id

        Returns:
            Role object or None if not found
        """

        role = await self.db.find_one({"_id": _id})
        if role is None:
            return None

        return Role(**role)

    async def create(self, role: Role) -> None:
        """Insert new role to the database

        Args:
            role: the role to insert
        """
        await self.db.insert_one(role.model_dump())
