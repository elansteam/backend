# pylint: disable=invalid-name
from __future__ import annotations

from utils.schemas import BaseModel
from db.types import types


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
        class get_orgs(BaseModel):
            organizations: list[types.Organization]
    class test:
        class signup(BaseModel):
            access_token: str
            refresh_token: str
        class orgs:
            class create(BaseModel):
                organization: types.Organization
