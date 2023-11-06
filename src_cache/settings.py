"""Конфигурационный файл проекта"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import typing

DATA_BASE_NAME = "ELAN"

ObjectId = typing.NewType("ObjectId", int)
"""ID объекта в базе данных"""
