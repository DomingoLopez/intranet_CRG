from pydantic import BaseModel


class AuthProgramData(BaseModel):
    num_empleado: str
    program: str