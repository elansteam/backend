from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import Config
from db.abstract_database_manager import AbstractDatabaseManager
import routers.users
import routers.auth
import routers.roles
import routers.groles
import routers.groups


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan (see https://fastapi.tiangolo.com/advanced/events/)
    In the application lifespan we need to connect and close connection to
    the database.
    
    Args:
        _app (FastAPI): application object. It is not using right now
    """
    # on startup
    AbstractDatabaseManager.connect_to_database(path=Config.db_path)
    yield
    # on shutdown
    AbstractDatabaseManager.close_database_connection()


app = FastAPI(title=Config.app_title, debug=True, lifespan=lifespan)

app.include_router(routers.users.router, prefix="/api/users")
app.include_router(routers.auth.router, prefix="/auth")
app.include_router(routers.roles.router, prefix="/api/roles")
app.include_router(routers.groles.router, prefix="/api/groles")
app.include_router(routers.groups.router, prefix="/api/groups")