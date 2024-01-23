"""Main project file"""

from loguru import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import Config
from db.helpers.abstract_database_manager import AbstractDatabaseManager
import routers.auth_router
import routers.group_roles_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan (see https://fastapi.tiangolo.com/advanced/events/)
    In the application lifespan we need to connect and close connection to
    the database.
    Args:
        _app (FastAPI): application object. It is not using right now
    """
    # TODO: add logger options

    # on startup
    AbstractDatabaseManager.connect_to_database(url=Config.db_connect_url)

    # await AbstractDatabaseManager.get_db()["Users"].insert_one({"users": "admin"})
    yield
    # on shutdown
    AbstractDatabaseManager.close_database_connection()


app = FastAPI(title=Config.app_title, debug=True, lifespan=lifespan)

app.include_router(routers.users_router.router, prefix="/api/users")
app.include_router(routers.auth_router.router, prefix="/auth")
app.include_router(routers.roles_router.router, prefix="/api/roles")
app.include_router(routers.group_roles_router.router, prefix="/api/group_roles")
app.include_router(routers.groups_router.router, prefix="/api/groups")
