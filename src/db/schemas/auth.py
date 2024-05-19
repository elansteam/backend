"""Schemas for auth"""
from pydantic import BaseModel


class TokenScheme(BaseModel):
    """JWT token pair scheme"""
    access_token: str
    refresh_token: str
