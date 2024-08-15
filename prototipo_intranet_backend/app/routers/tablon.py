# Imports de fastApi
import sys
import os
import numpy as np
from fastapi import APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Body
# Modelos
from ..db.models.m_hijos.modelo import Child
from ..db.models.m_menu.modelo import Menu
# Sesion
from ..db.session import get_db
# Tablas
from ..db.models.m_tablon.querys import get_tablon_db



# #############################################################
# Rutas para el menu
# #############################################################

# Prefjio del router
router = APIRouter(prefix="/tablon", tags=["tablon"])
@router.get("/")
def get_tablon(db: Session = Depends(get_db)):
    tablon = get_tablon_db(db)
    return tablon
    




