"""This file contains some helper handler functions"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger

from . import response


async def request_validation_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Unprocessable entity exception handler for make response consistent"""

    if not isinstance(exc, RequestValidationError):
        raise ValueError("Unexpected error: get wrong exception type")

    def detail_part_to_string(part: dict[str, str]):
        return (
            f"Type: {part.get('type', 'none')}; "
            f"Location: {', '.join(part.get('loc', 'none'))}; "
            f"Message: {part.get('msg', 'none')}; "
            f"Input: {part.get('input', 'none')}"
        )

    errors = "Unprocessable entity exception. Errors: " + "; ".join(
        [detail_part_to_string(error) for error in exc.errors()]
    )

    return JSONResponse(
        content={"ok": False, "error": {"code": response.ErrorCodes.UNPROCESSABLE_ENTITY.value, "message": errors}},
        status_code=422,
    )


async def error_response_handler(_request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, response.ErrorResponse):
        raise ValueError("Unexpected error: get wrong exception type")

    content: dict = {
        "ok": False,
        "error": {
            "code": exc.code.value,
        },
    }

    if exc.message is not None:
        content["error"]["message"] = exc.message
    elif exc.auto_message:
        content["error"]["message"] = exc.code.name

    return JSONResponse(content=content, status_code=exc.http_status_code)


async def internal_exception_handler(_request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "error": {"code": response.ErrorCodes.INTERNAL_SERVER_ERROR.value, "message": "Internal Server Error"},
        },
    )


async def external_not_found_handler(_request: Request, _exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "ok": False,
            "error": {"code": response.ErrorCodes.NOT_FOUND.value, "message": "Endpoint Not Found"},
        },
    )
