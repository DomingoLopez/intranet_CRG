from pydantic import BaseModel


class MenuFavData(BaseModel):
    id_menu: int
    id_empleado: str
    accion: bool