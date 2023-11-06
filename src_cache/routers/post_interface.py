"""Обработка post и put методов"""
from fastapi import APIRouter
from src.settings import ObjectId
from src.database.collections import contest, event, group, submit, task, user

router = APIRouter(
    prefix="/post",
    tags=["post", "put"],
)


class Creating:
    ...


class Changing:
    ...
