"""Some useful stuff"""


from enum import Enum
from typing import Literal
from typing import Any, Type
from pydantic import BaseModel
from starlette.responses import JSONResponse


def get_error_schema(description: str):  # deprecated
    """
    Args:
        description: error description

    Returns:
        special error schema in special format
    """
    return {"description": description,
            "content": {
                "application/json": {
                    "example": {
                        "status": "some status",
                        "response": {
                            "first_data": "example first",
                            "second_data": "example second"
                        }
                    },
                }
            }}


def get_error_response(status: str, data: dict[str, Any] | BaseModel | None = None,
                       status_code: int = 400) -> JSONResponse: # deprecated
    """
    Args:
        status: error status
        data: some useful data for error response. It may be a base model
        status_code: return status code

    Returns: JSONResponse, with exit code and message in special format
    """
    if data is None:
        data = {}

    if isinstance(data, BaseModel):
        data = data.model_dump(by_alias=True)

    response = JSONResponse(
        status_code=status_code,
        content={
            "status": status,
            "response": data
        }
    )
    return response


def get_response_model(model: Type[BaseModel] | Type[dict[str, Any]] =
                       dict[str, Any]) -> Type[BaseModel]: # deprecated
    """
    Return a pydantic custom model for response model.
    Use without argument to make response empty.
    Args:
        model: target template model
    """
    name = model.__name__

    response_model: Type[BaseModel] = type(f"ResponseModel{name}", (BaseModel,), {
        "__annotations__": {
            "status": Literal["OK"],
            "response": model
        }
    })

    return response_model


def get_response(model: BaseModel | dict[str, Any] | None = None) -> JSONResponse: # deprecated
    """
    Returns an object that should return API method
    Args:
        model: model that provides response form
    Returns:
    Object that should return API method
    """
    if model is None:
        model = {}
    if isinstance(model, BaseModel):
        model = model.model_dump(by_alias=True)

    return JSONResponse(status_code=200, content={
        "status": "OK",
        "response": model
    })


class ResponseErrorCodes(Enum):
    """
    Enum of response error codes.
    For description see documentation TODO: set documentation url
    """
    INTERNAL_SERVER_ERROR = 1
    UNPROCESSABLE_ENTITY = 2
    TOKEN_EXPIRED = 3
    TOKEN_VALIDATION_FAILED = 4
    COULD_NOT_FIND_USER_BY_TOKEN = 5

class ResponseWithErrorCode(Exception):
    """Response with custom error code"""

    code: ResponseErrorCodes
    message: str | None
    http_status_code: int
    auto_message: bool  # experemental
    """If main message is None, it makes message be error code representation"""

    def __init__(
        self,
        code: ResponseErrorCodes,
        message: str | None = None,
        http_status_code: int = 400,
        auto_message: bool = False
    ):
        self.code = code
        self.message = message
        self.http_status_code = http_status_code
        self.auto_message = auto_message
