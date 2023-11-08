from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.permission import Permission


class PermissionDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с правами доступа. Мутирующие методы не предусмотрены"""

    collection_name = Config.Collections.permissions

    async def get_by_name(self, name: str) -> Permission | None:
        """Получение права доступа по имени"""
        perm = await self.db.find_one({"name": name})

        if perm is None:
            return None

        return Permission.model_validate(perm)
