from db.abstract_database_manager import AbstractDatabaseManager
from db.models.role import Role
from db.models.user import User
from db.oid import OID
from bson import ObjectId
from pydantic import EmailStr
from config import Config


class UserDatabaseManager(AbstractDatabaseManager):
    """Методы базы данных с пользователями"""

    collection_name = Config.Collections.users

    async def create(self, user: User) -> None:
        """Создание пользователя в базе данных"""
        await self.db.insert_one({**user.model_dump()})

    async def get_by_id(self, oid: OID) -> User | None:
        """Получение пользователя по ID"""
        user = await self.db.find_one({"_id": ObjectId(oid)})
        if user is None:
            return None

        return User.model_validate(user)

    async def get_by_name(self, user_name: str) -> User | None:
        """Получение пользователя по user_name"""

        user = await self.db.find_one({"name": user_name})
        if user is None:
            return None
        return User.model_validate(user)

    async def get_by_email(self, email: EmailStr) -> User | None:
        """Получение пользователя по email"""

        user = await self.db.find_one({"email": email})
        if user is None:
            return None

        return User.model_validate(User)

    async def add_role(self, user_name: str, role_name: str) -> None:
        """Добавление пользователю роли."""

        await self.db.update_one({"name": user_name},
                                 {"$push": {"roles": role_name}})
