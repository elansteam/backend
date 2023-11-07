from fastapi import FastAPI
from src.config import Config
from db.abstract_database_manager import AbstractDatabaseManager
import routers.users
import uvicorn

app = FastAPI(title=Config.app_title, debug=True)

app.include_router(routers.users.router, prefix="/api/users")


@app.on_event("startup")
async def startup():
    """Старт"""
    AbstractDatabaseManager.connect_to_database(path=Config.db_path)


@app.on_event("shutdown")
async def shutdown():
    """Конец"""
    AbstractDatabaseManager.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
