"""GroupDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.group import Group
from config import Config


class GroupDatabaseManager(AbstractDatabaseManager):
    """Database methods with groups"""

    collection_name = Config.Collections.groups

    async def create(self, group: Group) -> None:
        """
        Creating new group in database
        Args:
            group: group object to create
        """

        await self.db.insert_one(group.model_dump())

    async def get_by_name(self, name: str) -> Group | None:
        """
        Getting group by name
        Args:
            name: group name to find

        Returns:
            Group object or None if not found
        """

        group = await self.db.find_one({"name": name})
        if group is None:
            return None
        return Group(**group)

    async def add_user(self, group_name: str, user_name: str) -> None:
        """
        Adding user to group members
        Args:
            group_name: where add user
            user_name: user to add
        """

        await self.db.update_one({"name": group_name},
                                 {"$set": {f"members.{user_name}": []}})

    async def add_grole(self, group_name: str, group_role_name: str) -> None:
        """
        Adding group_role to group
        Args:
            group_name: where add group_role
            group_role_name: role name to add
        """
        await self.db.update_one({"name": group_name},
                                 {"$push": {"group_roles": group_role_name}})

    async def get_members(self, group_name) -> list[str]:
        """
        Getting list of group members
        Args:
            group_name:
        Returns:
            list of usernames
        """

        members = await self.db.find_one({"name": group_name})

        return list(members["members"].keys())

    async def get_member_groles(self, group_name: str, user_name: str) -> list[str]:
        """
        Getting list of group roles of concrete group member
        Args:
            group_name: group, where user being
            user_name: user to get group roles
        Returns:
            list if group roles names, which has user with name user_name.
        """
        members = await self.db.find_one({"name": group_name})

        return members[user_name]
