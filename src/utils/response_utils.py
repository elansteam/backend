"""Some useful stuff"""

from starlette.responses import JSONResponse


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
