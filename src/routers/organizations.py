from fastapi import APIRouter, Depends

from db import methods
from src import types
from src.types import RQ, RS
from utils.auth.auth import get_current_user
from utils.response import ErrorCodes, ErrorResponse, SuccessfulResponse


router = APIRouter()


@router.get("/get", response_model=SuccessfulResponse[RS.organizations.get])
async def get(request: RQ.organizations.get = Depends(), _current_user: types.User = Depends(get_current_user)):
    if (organization := methods.get_organization(request.id)) is None:
        raise ErrorResponse(code=ErrorCodes.NOT_FOUND)

    return organization


@router.get("/get_members", response_model=SuccessfulResponse[RS.organizations.get_members])
async def get_members(
    request: RQ.organizations.get_members = Depends(), _current_user: types.User = Depends(get_current_user)
):
    return RS.organizations.get_members(members=methods.get_members_of_organization(request.id))
