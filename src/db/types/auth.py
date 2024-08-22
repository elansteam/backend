from utils.schemas import BaseModel


class JWTPair(BaseModel):
    access_token: str
    refresh_token: str
