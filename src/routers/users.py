from fastapi import APIRouter, Depends

from utils.response import SuccessfulResponse
from utils.auth import get_current_user
from db.types import types, RS


router = APIRouter()


@router.get("/current", response_model=SuccessfulResponse[RS.users.current])
async def current(current_user: types.User = Depends(get_current_user)):
    return RS.users.current(id=current_user.id, email=current_user.email, first_name=current_user.first_name)
