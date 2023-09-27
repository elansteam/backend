"""Основной файл"""
from backend.database.data_base import DataBase
from fastapi import FastAPI
import uvicorn

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, log_level="info")
