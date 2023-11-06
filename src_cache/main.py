# """Основной файл"""
from fastapi import FastAPI
from database.driver.driver import Driver
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import src.routers.get_interface
import src.routers.post_interface
import asyncio
import settings

app = FastAPI()

if __name__ == "__main__":
    app = FastAPI()

    # разрешенные сайты
    origins = ["http://localhost:63343"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # подключение роутеров
    app.include_router(src.routers.get_interface.router)
    app.include_router(src.routers.post_interface.router)

    Driver.init()
    uvicorn.run(app, log_level="info")
