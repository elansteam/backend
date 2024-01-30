"""Some useful stuff"""

from starlette.responses import JSONResponse
from typing import Any, Type
from pydantic import BaseModel


def get_error_schema(description: str):
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

    return JSONResponse(status_code=status_code, content={"status": status,
                                                          "response": data
                                                          })


def get_response_model(model: Type[BaseModel]) -> Type[BaseModel]:
    """
    Return a pydantic custom model for response model
    Args:
        model: target template model
    """
    response_model: Type[BaseModel] = type(f"ResponseModel{model.__name__}", (BaseModel,), {
        "__annotations__": {
            "status": str,
            "response": model
        }
    })
    return response_model


def get_response(model: BaseModel | dict[str, Any]) -> JSONResponse:
    if isinstance(model, BaseModel):
        model = model.model_dump(by_alias=True)
        
    return JSONResponse(status_code=200, content={
        "status": "OK",
        "response": model
    })
