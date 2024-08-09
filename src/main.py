from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import db
import routers
import routers.service
import utils.handlers
import utils.response
import utils.auth
from config import config


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting application")

    yield

    db.close_connection()
    logger.info("Shutting down application")


app = FastAPI(debug=config.debug, lifespan=lifespan)
app.include_router(routers.auth.router, prefix="/api/auth")
app.include_router(routers.service.router, prefix="/api/service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=config.debug,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_exception_handler(
    RequestValidationError,
    utils.handlers.request_validation_exception_handler
)

app.add_exception_handler(
    utils.response.ErrorResponse,
    utils.handlers.error_response_handler
)

app.add_exception_handler(
    500,
    utils.handlers.internal_exception_handler
)
