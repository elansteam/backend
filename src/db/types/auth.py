from pydantic import model_validator

from utils.schemas import BaseModel
from db.types.common import IntegerId, DomainName, Email


class JWTPair(BaseModel):
    access: str
    refresh: str

class SignInInput(BaseModel):
    id: IntegerId | None = None
    domain: DomainName | None = None
    email: Email | None = None
    password: str

    @model_validator(mode="after")
    def check_only_one_field(self):
        error_message = "You must provide exactly one of the fields: email, domain, user_id"
        assert ((self.id is None) +
               (self.domain is None) +
               (self.email is None) == 2), error_message
        return self
