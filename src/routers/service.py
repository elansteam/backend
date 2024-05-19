"""Service API methods"""

from fastapi import APIRouter, Depends
from utils.response_utils import ResponseWithErrorCode, ResponseErrorCodes
from auth import auth_user, Permissions

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

@router.get("/test/headers")
async def test_headers(current_user = Depends(auth_user(
    Permissions.CHANGE_USER_ROLES
))):
    """Returns error status"""
