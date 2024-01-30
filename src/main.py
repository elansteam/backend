"""Main project file"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import Config
import routers.auth_router
from db.MongoManager import MongoManager


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
    MongoManager.connect(Config.db_connect_url, Config.db_name)

    yield
    # on shutdown
    # await MongoManager.get_client().drop_database(Config.db_name)
    MongoManager.disconnect()


app = FastAPI(title=Config.app_title, debug=True, lifespan=lifespan)

app.include_router(routers.users_router.router, prefix="/api/users")
app.include_router(routers.auth_router.router, prefix="/auth")
app.include_router(routers.roles_router.router, prefix="/api/roles")
app.include_router(routers.groups_router.router, prefix="/api/groups")
