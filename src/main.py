from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

import db
import utils.handlers
import utils.middlewares
from config import config
import routers


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting application")

    yield
    db.close_connection()
    logger.info("Shutting down application")


app = FastAPI(title=config.app_title, debug=True, lifespan=lifespan)

app.include_router(routers.users.router, prefix="/api/users")
app.include_router(routers.auth.router, prefix="/api/auth")
app.include_router(routers.roles.router, prefix="/api/roles")
app.include_router(routers.groups.router, prefix="/api/groups")
app.include_router(routers.contests.router, prefix="/api/contests")
app.include_router(routers.problems.router, prefix="/api/problems")
app.include_router(routers.submissions.router, prefix="/api/submissions")
app.include_router(routers.service.router, prefix="/api/service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=config.debug,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=utils.middlewares.catch_internal_server_error
)

app.add_exception_handler(
    RequestValidationError,
    utils.handlers.request_validation_exception_handler
)

app.add_exception_handler(
    utils.response.ErrorResponse,
    utils.handlers.response_with_error_code_handler
)
