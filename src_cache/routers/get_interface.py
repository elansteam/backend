"""Обработка get методов"""
from fastapi import APIRouter
from src.settings import ObjectId
from src.database.collections import contest, event, group, submit, task, user

router = APIRouter(
    prefix="/get",
    tags=["get"],
)


class GetById:
    @staticmethod
    @router.get("/group/{group_id}", response_model=group.Group)
    async def get_group(group_id: ObjectId) -> group.Group:
        return "FIXME"

    @staticmethod
    @router.get("/user/{user_id}", response_model=user.User)
    async def get_user(user_id: ObjectId) -> user.User:
        return "FIXME"

    @staticmethod
    @router.get("/contest/{contest_id}", response_model=contest.Contest)
    async def get_contest(contest_id: ObjectId) -> contest.Contest:
        return "FIXME"

    @staticmethod
    @router.get("/submit/{submit_id}", response_model=submit.Submit)
    async def get_submit(submit_id: ObjectId) -> submit.Submit:
        return "FIXME"

    @staticmethod
    @router.get("/event/{event_id}", response_model=event.Event)
    async def get_event(event_id: ObjectId) -> event.Event:
        return "FIXME"

    @staticmethod
    @router.get("/task/{task_id}", response_model=task.Task)
    async def get_task(task_id: ObjectId) -> task.Task:
        return "FIXME"

# TODO: LONG POLLING
