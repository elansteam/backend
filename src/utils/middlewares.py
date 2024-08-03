from fastapi.responses import JSONResponse
from fastapi import Request
from loguru import logger

from utils.response import ErrorCodes


async def catch_internal_server_error(request: Request, call_next):
    """Middleware that catch all exceptions and format a JSON response"""
    try:
        return await call_next(request)
        # * Necessary here because we need catch all exceptions
    except Exception as exc: # pylint: disable=broad-exception-caught
        logger.exception(exc)
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "error": {
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                    "message": "Internal Server Error"
                }
            }
        )
