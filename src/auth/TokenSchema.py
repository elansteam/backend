from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Представление токенов"""
    access_token: str
    refresh_token: str