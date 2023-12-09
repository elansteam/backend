"""GroupRoleDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.group_role import GroupRole
from config import Config
from bson.objectid import ObjectId


class GroupRoleDatabaseManager(AbstractDatabaseManager):
    """Group roles database manager"""

    collection_name = Config.Collections.group_roles

    async def get_by_name(self, group_role_name: str, group_name: str) -> GroupRole | None:
        """Get group role by name

        Args:
            group_role_name (str): group role name
            group_name (str): group name

        Returns:
            group role or None if not found
        """
        group_role = await self.db.find_one({"name": group_role_name, "group": group_name})

        if group_role is None:
            return None

        return GroupRole(**group_role)

    async def get_by_id(self, _id: ObjectId) -> GroupRole | None:
        """
        Getting group role by id
        Args:
            _id: mongo object id

        Returns:
            group role object or None if not found
        """

        group_role = await self.db.find_one({"_id": _id})
        if group_role is None:
            return None

        return GroupRole(**group_role)

    async def create(self, group_role: GroupRole) -> None:
        """Insert new role to the database

        Args:
            group_role: role to insert
        """
        await self.db.insert_one(group_role.model_dump())
