# Imports de fastApi
import sys
import os
import numpy as np
from fastapi import APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Body
# Modelos
from ...core.models.request.auth_program_data import AuthProgramData

# Sesion
from ...db.session import get_db
# Tablas
from ...db.models.m_autorizaciones.querys import get_autorizaciones



# #############################################################
# Rutas para el menu
# #############################################################

# Prefjio del router
router = APIRouter(prefix="/auth_program", tags=["auth_program"])

@router.post("/")
def get_auth_program_data(auth_program_data: AuthProgramData, db: Session = Depends(get_db)):
    autorizacion = get_autorizaciones(auth_program_data, db)
    return autorizacion
    




