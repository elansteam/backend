"""This file contains some helper handler functions"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from auth.utils import AuthException
from utils import error_codes
from utils.response_utils import get_error_response

async def auth_exception_handler(_request: Request, exc: AuthException):
    """Authentication exception handler for make response consistent"""
    return get_error_response(
        status=exc.status,
        status_code=exc.status_code,
        data=exc.response
    )

async def request_validation_exception_handler(_request: Request, exc: RequestValidationError):
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
                "code": error_codes.UNPROCESSABLE_ENTITY,
                "message": errors
            }
        },
        status_code=422
    )
