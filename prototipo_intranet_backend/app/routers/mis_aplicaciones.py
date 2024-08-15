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
from ..db.models.m_misapps.querys import get_mis_apps_db



# #############################################################
# Rutas para el menu
# #############################################################

# Prefjio del router
router = APIRouter(prefix="/misaplicaciones", tags=["misaplicaciones"])
@router.get("/")
def get_mis_apps(db: Session = Depends(get_db)):
    mis_apps = get_mis_apps_db(db)
    return mis_apps
    




