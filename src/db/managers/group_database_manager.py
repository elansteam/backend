"""GroupDatabaseManager definition"""
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from db.models.group import Group
from config import Config
from db.models.group_role import GroupRole


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

    async def get(self, _id: int) -> Group | None:
        """
        Getting group by id
        Args:
            _id: mongo object id
        Returns:
            Group object or None if not found
        """
        group = await self.db.find_one({"_id": _id})
        if group is None:
            return None
        return Group(**group)

    async def add_user(self, group_id: int, user_id: int) -> None:
        """
        Adding user to group members
        Args:
            group_name: where add user
            user_name: user to add
        """
        await self.db.update_one({"_id": group_id},
                                 {"$set": {f"members.{user_id}": []}})

    async def add_role(self, group_role: GroupRole) -> None:
        """Adding group role to group

        Args:
            group_role (GroupRole): group role to add
        """
        # change format group<gid>_<rid> -> <rid>
        await self.db.update_one(
            {"_id": group_role.group},
            {"$push": {"group_roles": group_role.id.split("_")[1]}}
        )

    async def get_members(self, group_id: int) -> list[int]:
        """
        Getting list of group members
        Args:
            group_id: the group
        Returns:
            list of user ids
        """

        members = await self.db.find_one({"_id": group_id})
        if members is None:
            return list()
        return [int(user_id) for user_id in members["members"].keys()]

    async def get_member_roles(self, group_id: int, user_id: int) -> list[str]:
        """
        Getting list of group roles, which has user with given id
        Args:
            group_id: the group
            user_id: the user
        Returns:
            list if group roles names, which has user user with given id
        """
        members = await self.db.find_one({"_id": group_id})
        if members is None:
            return list()
        return members["members"][user_id]
