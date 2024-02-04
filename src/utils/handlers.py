"""This file contains some helper handler functions"""
from fastapi import Request
from auth.utils import AuthException
from utils.response_utils import get_error_response


async def auth_exception_handler(_request: Request, exc: AuthException):
    """Authentication exception handler for make response consistent"""
    return get_error_response(
        status=exc.status,
        status_code=exc.status_code,
        data=exc.response
    )
