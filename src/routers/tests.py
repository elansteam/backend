from fastapi import APIRouter


router = APIRouter()


@router.get("/test/ok")
async def test_ok():
    return {"some_result": "BANANA"}


@router.get("/test/validate_int/{_data}")
async def test_422(_data: int):
    return {}

@router.get("/test/500")
async def test_500():
    raise ValueError("This is ok")
