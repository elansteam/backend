from pydantic import Field

from utils.schemas import BaseModel
from .common import IntegerId, DomainName, Email, StringId

class User(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-295"""

    id: IntegerId = Field(alias='_id')
    domain: DomainName | None = Field(None)
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    mid_name: str | None = Field(None)
    groups: list[IntegerId] = []
    roles: list[StringId] = []
    hashed_password: str
    email: Email


class UserSignup(BaseModel):
    email: Email
    password: str
