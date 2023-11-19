"""Types for auth"""
from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Token base model"""
    access_token: str
    refresh_token: str
    # TODO: add expiration times
