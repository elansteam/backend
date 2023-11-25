"""GroupRoleDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.group_role import GroupRole
from config import Config


class GroupRoleDatabaseManager(AbstractDatabaseManager):
    """Group roles database manager"""

    collection_name = Config.Collections.groles

    async def get_by_name(self, group_role_name: str, group_name: str) -> GroupRole | None:
        """Get group role by name

        Args:
            group_role_name (str): group role name
            group_name (str): group name

        Returns:
            group role or None if not found
        """
        grole = await self.db.find_one({"name": group_role_name, "group": group_name})

        if grole is None:
            return None

        return GroupRole(**grole)

    async def create(self, group_role: GroupRole) -> None:
        """Insert new role to the database

        Args:
            group_role: role to insert
        """
        await self.db.insert_one(group_role.model_dump())
