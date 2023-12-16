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

    async def get_by_id(self, _id: int) -> Group | None:
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

    # async def add_group_role(self, group_id: int, group_role_id: str) -> None:
    #     """
    #     Adding group_role to group
    #     Args:
    #         group_id: group to add
    #         group_role_id: role name to add
    #     """
    #     await self.db.update_one({"name": group_name},
    #                              {"$push": {"group_roles": group_role_name}})

    async def get_members(self, group_id: int) -> list[int]:
        """
        Getting list of group members
        Args:
            group_id: the group
        Returns:
            list of user ids
        """

        members = await self.db.find_one({"_id": group_id})

        return (int(user_id) for user_id in members["members"].keys())

    async def get_member_group_roles(self, group_id: int, user_id: int) -> list[str]:
        """
        Getting list of group roles, which has user with given id
        Args:
            group_id: the group
            user_id: the user
        Returns:
            list if group roles names, which has user user with given id
        """
        members = await self.db.find_one({"_id": group_id})

        return members["members"][user_id]
