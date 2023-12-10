"""Some useful stuff"""

from starlette.responses import JSONResponse
from bson.objectid import ObjectId as _ObjectId
from pydantic.functional_validators import AfterValidator
from typing import Annotated


def check_object_id(value: str) -> str:
    """
    Validating object to be a ObjectId
    Args:
        value: object id like object
    Returns:
        value if validation is successful
    Raises:
        ValueError: if value - invalid object
    """
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]
"""A new representation of a ObjectId with validation"""


def get_error_schema(description: str, msg: str = "error msg"):
    """
    Args:
        description: error description
        msg: custom error message

    Returns:
        special error schema in special format
    """
    return {"description": description,
            "content": {
                "application/json": {
                    "example": {"detail": [{
                        "msg": msg,
                    }]},
                }
            }}


def get_error_response(msg: str, status_code: int = 400) -> JSONResponse:
    """
    Args:
        msg: error message
        status_code: return status code

    Returns: JSONResponse, with exit code and message in special format
    """
    return JSONResponse(status_code=status_code, content={"detail": [
        {"msg": msg}
    ]})
