"""Some useful stuff"""

from typing import Literal
from typing import Any, Type, Collection
from pydantic import BaseModel
from starlette.responses import JSONResponse


def get_error_schema(description: str) -> Collection[str]:
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
                       status_code: int = 400) -> JSONResponse:
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
                       dict[str, Any]) -> Type[BaseModel]:
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


def get_response(model: BaseModel | dict[str, Any] | None = None) -> JSONResponse:
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
