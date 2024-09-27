from fastapi import APIRouter, Depends

from utils.response import SuccessfulResponse
from utils.auth import get_current_user
from db import methods
from t import types, RS, RQ


router = APIRouter()


@router.get("/current", response_model=SuccessfulResponse[RS.users.current])
async def current(current_user: types.User = Depends(get_current_user)):
    return RS.users.current(id=current_user.id, email=current_user.email, first_name=current_user.first_name)


@router.get("/get_organizations", response_model=SuccessfulResponse[RS.users.get_organizations])
async def get_organizations(
    request: RQ.users.get_organizations = Depends(), _current_user: types.User = Depends(get_current_user)
):
    return RS.users.get_organizations(organizations=methods.get_organizations_by_user(request.id))
