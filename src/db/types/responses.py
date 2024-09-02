# pylint: disable=invalid-name
from __future__ import annotations
from utils.schemas import BaseModel


class RS:
    class auth:
        class signin(BaseModel):
            access_token: str
            refresh_token: str
        class refresh(BaseModel):
            access_token: str
            refresh_token: str
    class users:
        class current(BaseModel):
            id: int
            first_name: str
            email: str
    class test:
        class signup(BaseModel):
            class _User(BaseModel):
                id: str
                name: int
            access_token: str
            refresh_token: str
