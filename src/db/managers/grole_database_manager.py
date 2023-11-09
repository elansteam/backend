from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.grole import GRole


class GRoleDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с групповыми ролями"""

    collection_name = Config.Collections.groles

    async def get_by_name(self, name: str) -> GRole | None:
        """Получение роли по имени"""
        role = await self.db.find_one({"name": name})

        if role is None:
            return None

        return GRole.model_validate(role)

    async def create_role(self, role: GRole) -> None:
        """Создание роли в базе данных"""
        await self.db.insert_one({**role.model_dump()})
