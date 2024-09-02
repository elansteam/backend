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
            email: str | None  = None
            password: str

            @model_validator(mode="after")
            def check_only_one_field(self):
                error_message = "You must provide exactly one of the fields: email, domain, user_id"
                assert sum(x is not None for x in (
                    self.id, self.domain, self.email
                )) == 1, error_message
                return self
    class test:
        class signup(BaseModel):
            first_name: str = Field(..., max_length=30)
            email: Annotated[str, is_email]
            password: str
