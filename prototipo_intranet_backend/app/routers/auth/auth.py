# Imports de fastApi
import sys
import os
import numpy as np
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Body, Header

# Import para auth en AD
from ...connections.ad_conn import get_conn_AD, close_AD_conn, auth_AD

# Modelos necesarios
from ...core.models.request.login_data import LoginData
from ...core.models.response.login_response import LoginResponseOK
from ...core.models.user import User


# #############################################################
# Rutas para autorizaciones
# #############################################################

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/")
def login(login_data: LoginData):
    
    user = login_data.user
    password = login_data.password
    
    # Intentamos autenticar. 
    result = auth_AD(user, password)
    # Si result no es false, entonces es un objeto 
    # con los datos del usuario, creamos usuario y token
    # y devolvemos.    
    if result != False:
    # TODO: GENERAR TOKEN JWT
       login_res = LoginResponseOK(
            user=result,
            token='tokengenerado1234567891234569987874583548'
        )
    else:
        raise HTTPException(status_code=401, detail="Usuario o Contraseña no válidos")
        
    return login_res
    
    
    
@router.get("/checktoken")
def check_valid_token(authorization: str = Header(...)):
    # Si no hay cabecera con el token directamente error
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No Bearer token provided")
       
    
    # Lo siguiente, comprobar si se dispone de token válido en redis, etc y 
    # obtener el usuario para devolverlo
    token = authorization[len("Bearer "):]  
    # TODO: COMPROBAR SI TOKEN VÁLIDO
    
    # Crea la instancia de User usando argumentos con nombre
    user_instance = User(
        _id='1',
        id_empleado='U971574',
        centro='9352',
        nomcentro='C.I. Desarrollo',
        nombre='Domingo Jesús López Pacheco',
        isActive=True,
        roles=[]
    )
    # Crea la instancia de LoginResponseOK usando argumentos con nombre
    login_res = LoginResponseOK(
        user=user_instance,
        token=token
    )    
    
    return login_res
    


