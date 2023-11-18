from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.role import Role


class RoleDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с ролями"""

    collection_name = Config.Collections.roles

    async def get_by_name(self, name: str) -> Role | None:
        """Получение роли по имени"""
        role = await self.db.find_one({"name": name})

        if role is None:
            return None

        return Role(**role)

    async def create(self, role: Role) -> None:
        """Создание роли в базе данных"""
        await self.db.insert_one({**role.model_dump()})


