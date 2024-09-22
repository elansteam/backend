from fastapi import APIRouter, Depends

from db.types import RQ, RS, types
from db import methods
from utils.auth.auth import get_current_user
from utils.response import SuccessfulResponse

router = APIRouter()


@router.get("/get", response_model=SuccessfulResponse[RS.groups.get])
async def get(request: RQ.groups.get = Depends(), _current_user: types.User = Depends(get_current_user)):
    return methods.groups.get(request.id)
