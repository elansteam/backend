"""Service API methods"""

from fastapi import APIRouter


router = APIRouter()


@router.get("/ping")
async def ping():
    """Ping - pong method"""
    return {"message": "pong"}
