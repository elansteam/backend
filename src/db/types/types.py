from typing import Literal
from pydantic import Field

from utils.schemas import BaseModel


class Member(BaseModel):
    id: int
    roles: list[str] = []
    custom_permissions: int = 0

class Role(BaseModel):
    id: str
    name: str
    permissions: int

class   (BaseModel):
    members: list[Member]
    roles: list[Role] = []

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

class _OrganizationBase(_HasMembersWithRoles):
    name: str

class Organization(_OrganizationBase):
    id: int = Field(alias='_id')

class OrganizationWithoutID(_OrganizationBase):
    ...
