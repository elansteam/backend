# pylint: disable=invalid-name
from __future__ import annotations

from utils.schemas import BaseResponse
from db.types import types


class RS:
    class auth:
        class signin(BaseResponse):
            access_token: str
            refresh_token: str
        class refresh(BaseResponse):
            access_token: str
            refresh_token: str
    class users:
        class current(BaseResponse):
            id: int
            first_name: str
            email: str
        class get_organizations(BaseResponse):
            organizations: list[types.Organization]
    class organizations:
        class get(types.Organization, BaseResponse):
            ...
    class test:
        class signup(BaseResponse):
            access_token: str
            refresh_token: str
        class organizations:
            class create(types.Organization, BaseResponse):
                ...
