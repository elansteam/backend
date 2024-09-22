# pylint: disable=invalid-name
from __future__ import annotations
from typing import Annotated
from pydantic import model_validator, Field

from utils.schemas import BaseModel
from .validators import is_email


class RQ:
    class auth:
        class signin(BaseModel):
            id: int | None = None
            domain: str | None = None
            email: str | None = None
            password: str

            @model_validator(mode="after")
            def check_only_one_field(self):
                error_message = "You must provide exactly one of the fields: email, domain, user_id"
                assert sum(x is not None for x in (self.id, self.domain, self.email)) == 1, error_message
                return self

    class organizations:
        class get(BaseModel):
            id: int

        class get_groups(BaseModel):
            id: int

    class users:
        class get_organizations(BaseModel):
            id: int

    class groups:
        class get(BaseModel):
            id: int

    class test:
        class signup(BaseModel):
            first_name: str = Field(..., max_length=30)
            email: Annotated[str, is_email]
            password: str

        class organizations:
            class create(BaseModel):
                name: str = Field(..., max_length=30)

            class invite(BaseModel):
                organization_id: int
                user_id: int

        class groups:

            class create(BaseModel):
                name: str = Field(..., max_length=30)
                organization_id: int

            class invite(BaseModel):
                user_id: int
                group_id: int
