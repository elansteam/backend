from fastapi import APIRouter

from utils.response import SuccessfulResponse


router = APIRouter()


@router.get("/ping", response_model=SuccessfulResponse[None])
async def ping():
    return
