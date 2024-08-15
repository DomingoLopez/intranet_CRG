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
from ..db.models.m_avisos.querys import get_avisos_db



# #############################################################
# Rutas para el menu
# #############################################################

# Prefjio del router
router = APIRouter(prefix="/avisos", tags=["aviso"])
@router.get("/")
def get_avisos(db: Session = Depends(get_db)):
    avisos = get_avisos_db(db)
    return avisos
    




