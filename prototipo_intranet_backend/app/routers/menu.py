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
from ..db.models.m_menu.querys import get_menu_db
from ..db.models.m_hijos.querys import get_hijos_db

# #############################################################
# Funciones auxiliares
# #############################################################


def generar_estructura_menu(menu_data, childs_data, id_menu_principal):
    '''
    Esta función es la que compone el menú de manera recursiva. 
    Habría que observarla y ver si merece la pena habilitar una base de datos
    en cache como Redis (que seguramente sí para tema de tokens), para mantener
    la estructura del menú en caché, y que solo se cambie la estructura cuando 
    haya una alteración en los activos de información.
    '''
    # Funcion auxiliar para obtener los hijos de un menu dado
    def obtener_hijos(menu_id):
        return [Child(child.id_menu, child.id_child, child.order) for child in childs_data if child.id_menu == menu_id]
    
    # Esto es como lo hacía antes
    # # Funcion recursiva para construir los objetos Menu
    # def construir_menu(menu_id):
    #     menu_info = next((item for item in menu_data if item.id_menu == menu_id), None)
    #     if menu_info is None:
    #         return None  
    #     childs = obtener_hijos(menu_id)
    #     childs_menus = [construir_menu(child.id_child) for child in childs]
    #     return Menu(menu_info.id_menu, menu_info.label.strip(), menu_info.categoria.strip(), menu_info.tipo_activo.strip(),
    #                 menu_info.url.strip(), menu_info.order, menu_info.permitir_fav, menu_info.is_fav, menu_info.ruta ,childs_menus)

    # # Construir la estructura de menu a partir del menu raiz (id_menu = 1)
    # return construir_menu(id_menu_principal)
    
    # Funcion recursiva para construir los objetos Menu
    def construir_menu(menu_id, ruta_padre=""):
            menu_info = next((item for item in menu_data if item.id_menu == menu_id), None)
            if menu_info is None:
                return None
            
            # Construir la ruta actual concatenando la del padre con el label del menú actual
            ruta_actual = f"{ruta_padre} > {menu_info.label.strip()}" if ruta_padre else menu_info.label.strip()
            
            childs = obtener_hijos(menu_id)
            childs_menus = [construir_menu(child.id_child, ruta_actual) for child in childs]
            
            return Menu(menu_info.id_menu, menu_info.label.strip(), menu_info.categoria.strip(), menu_info.tipo_activo.strip(),
                        menu_info.url.strip(), menu_info.order, menu_info.permitir_fav, menu_info.is_fav, ruta_actual, childs_menus)

        # Construir la estructura de menú a partir del menú raíz (id_menu_principal)
    return construir_menu(id_menu_principal)





# #############################################################
# Rutas para el menu
# #############################################################

# Prefjio del router
router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/")
def get_menu(db: Session = Depends(get_db)):
    menu = get_menu_db(db)
    childs = get_hijos_db(db)
    # Obtenemos los que tienen ID_MENU = 0, que son los que 
    # no tienen padre.
    id_menus_principales = [item.id_child for item in childs if item.id_menu == 0]
    
    menu_construido = []
    for i,id in enumerate(id_menus_principales):
        menu_construido.append(generar_estructura_menu(menu, childs, id))
    
    return menu_construido
    




