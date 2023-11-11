from fastapi import FastAPI
from src.config import Config
from db.abstract_database_manager import AbstractDatabaseManager
import routers.users
import routers.auth
import routers.roles
import routers.groles
import routers.groups

app = FastAPI(title=Config.app_title, debug=True)

app.include_router(routers.users.router, prefix="/api/users")
app.include_router(routers.auth.router, prefix="/auth")
app.include_router(routers.roles.router, prefix="/api/roles")
app.include_router(routers.groles.router, prefix="/api/groles")
app.include_router(routers.groups.router, prefix="/api/groups")


@app.on_event("startup")
async def startup():
    """Старт"""
    AbstractDatabaseManager.connect_to_database(path=Config.db_path)


@app.on_event("shutdown")
async def shutdown():
    """Конец"""
    AbstractDatabaseManager.close_database_connection()