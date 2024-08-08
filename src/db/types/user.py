from pydantic import Field

from utils.schemas import BaseModel
from .common import Email

class User(BaseModel):
    """https://app.clickup.com/9015604104/v/dc/8cnycw8-115/8cnycw8-295"""

    id: int = Field(alias='_id')
    domain: str | None = Field(None)
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    mid_name: str | None = Field(None)
    groups: list[int] = []
    roles: list[str] = []
    hashed_password: str
    email: str


class UserSignup(BaseModel):
    email: Email
    password: str
