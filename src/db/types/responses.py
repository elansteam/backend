from utils.schemas import BaseModel


class AuthSignin(BaseModel):
    access_token: str
    refresh_token: str

class AuthSignup(BaseModel):
    access_token: str
    refresh_token: str