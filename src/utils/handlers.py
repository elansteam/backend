"""This file contains some helper handler functions"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from . import response_utils


async def request_validation_exception_handler(
    _request: Request,
    exc: RequestValidationError
):
    """Unprocessable entity exception handler for make response consistent"""

    def detail_part_to_string(part: dict[str, str]):
        return (
            f"Type: {part['type']}\n"
            f"Location: {', '.join(part['loc'])}\n"
            f"Message: {part['msg']}\n"
            f"Input: {part['input']}\n"
            f"Url: {part['url']}\n"
        )

    errors = "Unprocessable entity exception. Errors:\n" + \
        '\n'.join([detail_part_to_string(error) for error in exc.errors()])

    return JSONResponse(
        content={
            "ok": False,
            "error": {
                "code": response_utils.ResponseErrorCodes.UNPROCESSABLE_ENTITY.value,
                "message": errors
            }
        },
        status_code=422
    )

async def response_with_error_code_handler(
    _request: Request,
    exc: response_utils.ResponseWithErrorCode
) -> JSONResponse:
    """Handle response with error code"""

    content: dict = {
        "ok": False,
        "error": {
            "code": exc.code.value,
        }
    }

    if exc.message is not None:
        content["error"]["message"] = exc.message
    elif exc.auto_message:
        content["error"]["message"] = exc.code.name

    return JSONResponse(
        content=content,
        status_code=exc.http_status_code
    )
