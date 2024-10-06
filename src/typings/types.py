from utils.schemas import BaseModel


# Misc
class Member(BaseModel):
    object_id: int
    target_id: int


class JWTPair(BaseModel):
    access_token: str
    refresh_token: str


# Users
class _UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    hashed_password: str
    email: str


class UserWithoutID(_UserBase): ...


class User(_UserBase):
    id: int


# Organizations
class _OrganizationBase(BaseModel):
    name: str


class Organization(_OrganizationBase):
    id: int


class OrganizationWithoutID(_OrganizationBase): ...
