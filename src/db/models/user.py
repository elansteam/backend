from pydantic import BaseModel, EmailStr
from src.db.oid import OID
from bson import ObjectId


class User(BaseModel):
    """Модель пользователя в базе данных"""

    _id: ObjectId
    """Уникальный идентификатор пользователя"""

    user_name: str
    """Идентификатор пользователя"""

    password_hash: str
    """SHA-256 хеш пароля"""

    email: EmailStr
    """Уникальный адрес электронной почты"""

    first_name: str
    """Имя"""

    last_name: str
    """Фамилия"""

    mid_name: str | None
    """Отчество"""

    # TODO: ADD BELOW IN FUTURE

    # groups: List[ObjectId]
    # """Группы, в которых состоит пользователь"""

    # roles: List[Role]
    # """Список ролей пользователя"""
    # # permission: int
    # # """Уровень доступа пользователя:
    # # 0 - Нулевой
    # # 1 - Пользователь может создавать группы
    # # 3 - Пользователь может создавать задачи
    # # 2 - Пользователь админ"""
