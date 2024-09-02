from typing import Literal

from pydantic import Field
from utils.schemas import BaseModel


class JWTPair(BaseModel):
    access_token: str
    refresh_token: str

EntityTargetType = Literal["user", "group", "contest"]

class Entity(BaseModel):
    id: str = Field(alias='_id')
    target_type: EntityTargetType
    target_id: int

class _UserBase(BaseModel):
    domain: str | None = None
    first_name: str
    last_name: str | None = None
    groups: list[int] = []
    hashed_password: str
    email: str

class UserWithoutID(_UserBase):
    ...

class User(_UserBase):
    id: int = Field(alias='_id')
