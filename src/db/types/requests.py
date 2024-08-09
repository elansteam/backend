from typing import Annotated
from pydantic import model_validator
from utils.schemas import BaseModel

from .common import is_email


class AuthSignin(BaseModel):
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

class AuthSignup(BaseModel):
    first_name: str  # TODO: set validation here
    email: Annotated[str, is_email]
    password: str
