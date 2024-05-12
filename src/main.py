"""Main project file"""

from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from utils.handlers import auth_exception_handler
from auth.utils import AuthException
from config import config
import routers

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan (see https://fastapi.tiangolo.com/advanced/events/)
    In the application lifespan we need to connect and close connection to
    the database.
    Args:
        _app (FastAPI): application object. It is not using right now
    """

    # on startup
    logger.info("Starting application")

    yield
    # on shutdown
    logger.info("Shutting down application")


app = FastAPI(title=config.app_title, debug=True, lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(routers.users.router, prefix="/api/users")
app.include_router(routers.auth.router, prefix="/api/auth")
app.include_router(routers.roles.router, prefix="/api/roles")
app.include_router(routers.groups.router, prefix="/api/groups")
app.include_router(routers.contests.router, prefix="/api/contests")
app.include_router(routers.problems.router, prefix="/api/problems")
app.include_router(routers.submissions.router, prefix="/api/submissions")
app.include_router(routers.service.router, prefix="/api/service")

# exception handlers
app.add_exception_handler(AuthException, auth_exception_handler)
