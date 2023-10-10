# """Основной файл"""
from fastapi import FastAPI
from database.driver.driver import Driver
import uvicorn
import asyncio
import settings

app = FastAPI()

if __name__ == "__main__":
    Driver.init()
    uvicorn.run(app, log_level="info")
