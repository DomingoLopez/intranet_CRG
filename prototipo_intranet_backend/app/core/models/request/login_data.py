from pydantic import BaseModel


class LoginData(BaseModel):
    user: str
    password: str