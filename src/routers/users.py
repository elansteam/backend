from fastapi import APIRouter, Depends

from utils.auth import get_current_user
from utils.response import SuccessfulResponse
from db import types
from db.types import responses as RS


router = APIRouter()

@router.get("/current", response_model=SuccessfulResponse[RS.UsersCurrent])
async def current(current_user: types.user.User = Depends(get_current_user)):
    return RS.UsersCurrent(
        id=current_user.id,
        first_name=current_user.first_name,
        email=current_user.email
    )
