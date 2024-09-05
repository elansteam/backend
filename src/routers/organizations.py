from fastapi import APIRouter, Depends

from db import methods
from db.types import types, RQ, RS
from utils.auth.auth import get_current_user
from utils.response import SuccessfulResponse


router = APIRouter()


@router.get("/get", response_model=SuccessfulResponse[RS.orgs.get])
async def get(request: RQ.orgs.get = Depends(), _current_user: types.User = Depends(get_current_user)):
    organization = methods.
