from fastapi import APIRouter, Depends

from db import methods
from db.types import types, RQ, RS
from utils.auth.auth import get_current_user
from utils.response import ErrorCodes, ErrorResponse, SuccessfulResponse


router = APIRouter()


@router.get("/get", response_model=SuccessfulResponse[RS.organizations.get])
async def get(request: RQ.organizations.get = Depends(), _current_user: types.User = Depends(get_current_user)):
    if (organization := methods.helpers.get_object_by_id(request.id, types.Organization)) is None:
        raise ErrorResponse(code=ErrorCodes.ENTITY_NOT_FOUND)

    return organization
