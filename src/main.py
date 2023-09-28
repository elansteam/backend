"""Основной файл"""
from fastapi import FastAPI
from database.driver.driver import Driver
import uvicorn
import routers.create
import asyncio

app = FastAPI()
app.include_router(routers.create.router)

if __name__ == "__main__":
    Driver.init()
    uvicorn.run(app, log_level="info")
