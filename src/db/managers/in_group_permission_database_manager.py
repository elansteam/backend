from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.in_group_permission import InGroupPermission


class InGroupPermissionDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с групповыми разрешениями"""

    collection_name = Config.Collections.in_group_permissions

    async def get_by_name(self, name: str) -> InGroupPermission | None:
        """Получение разрешения по имени"""
        perm = await self.db.find_one({"name": name})

        if perm is None:
            return None

        return InGroupPermission.model_validate(perm)
