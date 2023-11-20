"""UserDatabaseManager definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.user import User
from config import Config


class UserDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с пользователями"""

    collection_name = Config.Collections.users

    async def create(self, user: User) -> None:
        """Создание пользователя в базе данных"""
        await self.db.insert_one({**user.model_dump()})

    async def get_by_name(self, user_name: str) -> User | None:
        """Получение пользователя по user_name"""

        user = await self.db.find_one({"name": user_name})
        if user is None:
            return None
        return User(**user)

    async def add_role(self, user_name: str, role_name: str) -> None:
        """Добавление пользователю роли"""

        await self.db.update_one({"name": user_name},
                                 {"$push": {"roles": role_name}})
