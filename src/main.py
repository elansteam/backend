from fastapi import FastAPI
from config import Config
from db import DatabaseManager
import uvicorn

app = FastAPI(title="Async FastAPI")


# app.include_router(posts.router, prefix='/api/posts')

@app.on_event("startup")
async def startup():
    config = Config()
    DatabaseManager().connect_to_database(path=config.db_path)


@app.on_event("shutdown")
async def shutdown():
    DatabaseManager().close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
