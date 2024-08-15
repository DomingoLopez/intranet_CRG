from pydantic import BaseModel
from ..user import User


class LoginResponseOK(BaseModel):
    user: User 
    token: str
