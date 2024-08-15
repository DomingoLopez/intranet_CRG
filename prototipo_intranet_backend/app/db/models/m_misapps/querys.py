from sqlalchemy import text
from sqlalchemy.orm import Session
from .mapeo import mapea_resultado
from .modelo import MiAplicacion

import pandas as pd
import numpy as np


def get_mis_apps_db(db: Session):
    '''
    Conteo de publicaciones por fecha del tipo 1 y 2 de normativa
    que están visibles, agrupadas por fecha de los últimos 3 días,
    para poder mostrar correctamente la normativa con estas casuísticas
    '''
    
    try:
        # AQUÍ vamos a devolver valores Dummies hasta que veamos cómo enfocar el tema
        result = [ [1, "Desbloqueo usuarios windows", "http://SERVER/Autorizaciones/CreaUrl.php?USUARIO=1465&PROG=VERFALLIDOSDOT0S" ],
                   [2, "Admin. Blog Cuéntame", "http://SERVER/Autorizaciones/CreaUrl.php?USUARIO=1465&PROG=VERFALLIDOSDOT0S" ],
                   [3, "Consultas SSCC", "http://SERVER/Autorizaciones/CreaUrl.php?USUARIO=1465&PROG=VERFALLIDOSDOT0S" ],
                   [4, "Sigpe Interno", "http://SERVER/Autorizaciones/CreaUrl.php?USUARIO=1465&PROG=VERFALLIDOSDOT0S" ],
                   [5, "Tasaciones", "http://SERVER/Autorizaciones/CreaUrl.php?USUARIO=1465&PROG=VERFALLIDOSDOT0S" ], 
                   
                ]
        
        misapps = [MiAplicacion(
        id = row[0],
        titulo = row[1].strip(),
        url = row[2].strip()
        ) for row in result]
        
        
    except Exception as e : 
        print(f"Error al obtener fechas agrupadas de normativa: {e}")
        misapps = []
        
    return misapps
    