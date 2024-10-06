# pylint: disable=invalid-name
from __future__ import annotations

from utils.schemas import BaseModel
from typings import types


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

        class get_organizations(BaseModel):
            organizations: list[types.Organization]

    class organizations:
        class get(types.Organization): ...

        class get_members(BaseModel):
            members: list[int]

    class test:
        class signup(BaseModel):
            access_token: str
            refresh_token: str

        class organizations:
            class create(types.Organization): ...