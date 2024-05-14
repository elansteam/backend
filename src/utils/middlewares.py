"""Global middlewares and handlers"""

import json
from loguru import logger
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import _StreamingResponse

from utils import error_codes

async def format_successful_json_response(request: Request, call_next):
    """Middleware that format a successful JSON response"""
    response: _StreamingResponse = await call_next(request)
    content_type = response.headers.get("content-type")

    if content_type != "application/json" or response.status_code != 200:
        return response

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    return JSONResponse(content={
        "ok": True,
        "response": json.loads(response_body.decode())
    })


async def catch_internal_server_error(request: Request, call_next):
    """Middleware that catch all exceptions and format a JSON response"""
    try:
        return await call_next(request)

        # Necessary here because we need catch all exceptions
    except Exception as exc: # pylint: disable=broad-exception-caught
        logger.exception(exc)
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "error": {
                    "code": error_codes.INTERNAL_SERVER_ERROR,
                    "error": "Internal server error"
                }
            }
        )
    