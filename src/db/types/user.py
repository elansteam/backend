from pydantic import Field

from utils.schemas import BaseModel


class _UserBase(BaseModel):
    domain: str | None = None
    first_name: str
    groups: list[int] = []
    roles: list[str] = []
    hashed_password: str
    email: str

class UserWithoutID(_UserBase):
    ...

class User(_UserBase):
    id: int = Field(alias='_id')
