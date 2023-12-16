"""GroupRoleDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.group_role import GroupRole
from config import Config


class GroupRoleDatabaseManager(AbstractDatabaseManager):
    """Group roles database manager"""

    collection_name = Config.Collections.group_roles

    async def get(self, group_id: int, group_role_name: str) -> GroupRole | None:
        """Get group role by name

        Args:
            group_id: the group
            group_role_name (str): group role name

        Returns:
            group role or None if not found
        """
        group_role = await self.db.find_one({"_id": f"group{group_id}_{group_role_name}"})

        if group_role is None:
            return None

        return GroupRole(**group_role)

    async def create(self, group_role: GroupRole) -> None:
        """Insert new role to the database

        Args:
            group_role: role to insert
        """
        await self.db.insert_one(group_role.model_dump())
