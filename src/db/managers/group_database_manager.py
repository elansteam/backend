from db.abstract_database_manager import AbstractDatabaseManager
from db.models.role import Role
from db.models.group import Group
from db.oid import OID
from bson import ObjectId
from pydantic import EmailStr
from config import Config


class GroupDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с пользователями"""

    collection_name = Config.Collections.groups

    async def create(self, group: Group) -> None:
        """Создание группы в базе данных"""

        await self.db.insert_one({
            **group.model_dump()
        })

    async def get_by_name(self, name: str) -> Group | None:
        """Получение группы по имени"""

        group = await self.db.find_one({"name": name})
        if group is None:
            return None
        return Group.model_validate({**group})

    async def add_user(self, group_name: str, user_name: str) -> None:  # FIXME
        """Добавить пользователя в группу"""

        await self.db.update_one({"name": group_name},
                                 {})

    async def add_grole(self, group_name: str, grole_name: str):
        """Добавляет grole в группу"""
        await self.db.update_one({"name": group_name},
                                 {"$push": {"groles": grole_name}})
