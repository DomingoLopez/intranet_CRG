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
from ..db.models.m_normativa.querys import get_total_conteo_fechas_db, get_normativa_db



# #############################################################
# Rutas para el menu
# #############################################################

# Prefjio del router
router = APIRouter(prefix="/normativa", tags=["normativa"])
@router.get("/")
def get_normativa(db: Session = Depends(get_db)):
    normativa = get_normativa_db(db)
    return normativa
    




