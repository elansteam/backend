from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.grole import GRole


class GRoleDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с групповыми ролями"""

    collection_name = Config.Collections.groles

    async def get_by_name(self, grole_name: str, group_name: str) -> GRole | None:
        """Получение grole по имени"""
        grole = await self.db.find_one({"name": grole_name, "group": group_name})

        if grole is None:
            return None

        return GRole(**grole)

    async def create(self, grole: GRole) -> None:
        """Создание grole в базе данных"""
        await self.db.insert_one({**grole.model_dump()})
