"""Service API methods"""

from fastapi import APIRouter
from utils.response_utils import ResponseWithErrorCode, ResponseErrorCodes


router = APIRouter()


@router.get("/test/ok")
async def test_ok():
    """Returns ok status"""
    return {"some_result": "BANANA"}


@router.get("/test/validate_int/{_data}")
async def test_422(_data: int):
    """Returns error status"""
    return {}

@router.get("/test/500")
async def test_500():
    """Returns error status"""
    raise ValueError("This is ok")
