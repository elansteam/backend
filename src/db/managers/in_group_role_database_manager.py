from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.in_group_role import InGroupRole


class InGroupRoleDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с групповыми ролями"""

    collection_name = Config.Collections.in_group_roles

    async def get_by_name(self, name: str) -> InGroupRole | None:
        """Получение роли по имени"""
        role = await self.db.find_one({"name": name})

        if role is None:
            return None

        return InGroupRole.model_validate(role)

    async def create_role(self, role: InGroupRole) -> None:
        """Создание роли в базе данных"""
        await self.db.insert_one({**role.model_dump()})
