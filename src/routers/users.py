from fastapi import APIRouter, Depends
from db.oid import OID
from db.managers.user_database_manager import UserDatabaseManager

from src.db.models.user import User

router = APIRouter()

db = UserDatabaseManager()


@router.get("/get_by_id/{oid}")
async def get_by_id(oid: OID):
    # user = await db.get_user_by_id(oid)
    user = await db.get_by_id(oid)
    return user.__dict__
