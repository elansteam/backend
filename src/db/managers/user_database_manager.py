from db.abstract_database_manager import AbstractDatabaseManager
from db.models.user import User
from db.oid import OID
from bson import ObjectId
from config import Config


class UserDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с пользователями"""

    collection_name = Config.Collections.users

    async def create(self, user: User) -> None:
        """Создание пользователя в базе данных"""

    async def get_by_id(self, oid: OID) -> User:
        """Получение пользователя по ID"""
        x = await self.db.find_one({"_id": ObjectId(oid)})

        return User.model_validate(x)
