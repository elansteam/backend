from fastapi import APIRouter, Depends, Path
from db.oid import OID
from db.managers.user_database_manager import UserDatabaseManager

from src.db.models.user import User

router = APIRouter()

db = UserDatabaseManager()


@router.get("/get_by_id/{oid}", response_model=User)
async def get_by_id(oid: str = Path(..., description="Идентификатор пользователя ObjectId")):
    """Получение пользователя по ID"""
    user = await db.get_by_id(OID(oid))
    return user
