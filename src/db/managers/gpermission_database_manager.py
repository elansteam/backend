from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.gpermission import GPermission


class GPermissionDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с групповыми разрешениями"""

    collection_name = Config.Collections.gpermissions

    async def get_by_name(self, name: str) -> GPermission | None:
        """Получение разрешения по имени"""
        perm = await self.db.find_one({"name": name})

        if perm is None:
            return None

        return GPermission.model_validate(perm)
