from pydantic import BaseModel

class User(BaseModel): 
    
    _id: str
    id_empleado: str
    centro: str
    nomcentro: str
    nombre: str
    isActive: bool
    roles: list
    