# Imports de fastApi
import sys
import os
import numpy as np
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Body, Header

# Sesion
from ..db.session import get_db
# Modelos
from ..core.models.request.menu_fav_data import MenuFavData
# DB
from ..db.models.m_menu.querys import insertMenuFav, deleteMenuFav



# #############################################################
# Rutas para autorizaciones
# #############################################################

router = APIRouter(prefix="/fav", tags=["fav"])

@router.post("/")
def updateMenuFav(fav_data: MenuFavData, db: Session = Depends(get_db)):
    
    id_empleado = fav_data.id_empleado
    id_menu = fav_data.id_menu
    accion = fav_data.accion
    
    try:
        if accion==True:
            result = insertMenuFav(id_empleado, id_menu, db)
        else:
            result = deleteMenuFav(id_empleado, id_menu, db)
    except Exception as e : 
        raise HTTPException(status_code=503, detail="Error al insertar o eliminar favorito")
    
    return result

    


