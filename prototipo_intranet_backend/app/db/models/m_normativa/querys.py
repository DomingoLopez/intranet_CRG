from sqlalchemy import text
from sqlalchemy.orm import Session
from .mapeo import mapea_resultado

import pandas as pd
import numpy as np


def get_total_conteo_fechas_db(db: Session):
    '''
    Conteo de publicaciones por fecha del tipo 1 y 2 de normativa
    que están visibles, agrupadas por fecha de los últimos 3 días,
    para poder mostrar correctamente la normativa con estas casuísticas
    '''
    
    total_publicaciones = 0
    dia_ini = '11/11/1111'
    dia_fin = '11/11/1111'
    
    try:
        # #############################################
        # 1ª Query conteo de noticias por día
        sql_query = text("SELECT COUNT(*) AS TOTAL,  \
                            FECHA AS FECHA \
                            FROM CPD.TABLA \
                            WHERE ID_TIPO IN(1,2) \
                            AND VISIBLE = 1 \
                            GROUP BY FECHA \
                            ORDER BY FECHA DESC \
                            FETCH FIRST 3 ROWS ONLY")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        df = pd.DataFrame(result.fetchall(),columns=result.keys())

        # sumamos el total de los últimos 3 días
        total_publicaciones = df['total'].sum()
        # obtenemos día inicial y final
        dia_ini = df.iloc[0, 1].strftime("%d/%m/%Y")
        dia_fin = df.iloc[2, 1].strftime("%d/%m/%Y")
        
        
    except Exception as e : 
        print(f"Error al obtener fechas agrupadas de normativa: {e}")

    return total_publicaciones, dia_ini, dia_fin
    




def get_normativa_db(db: Session):
    '''
    Obtenemos la normativa con los filtros indicados. 
    '''
    
    total_publicaciones, dia_ini, dia_fin = get_total_conteo_fechas_db(db)
    
    if(total_publicaciones > 5):
        
        sql_query = text(f"SELECT \
                            A.ID_NOVED, \
                            A.FECHA,  \
                            TP.NOMBRE AS TIPO, \
                            A.TITULO, \
                            VARCHAR(SUBSTR(A.URL,1,1000)) AS URL, \
                            TP.ORDEN_TIPO \
                            FROM\
                            (SELECT * FROM CPD.TABLA \
                            WHERE VISIBLE=1 AND FECHA <='{dia_ini}'AND FECHA >= '{dia_fin}' \
                            AND ID_TIPO IN (1,2)) AS A \
                            JOIN \
                            (SELECT * FROM CPD.TABLA2 WHERE ID_TIPO IN (1,2)) AS TP\
                            ON A.ID_TIPO = TP.ID_TIPO \
                            UNION \
                            SELECT \
                            A.ID_NOVED, \
                            A.FECHA,  \
                            TP.NOMBRE AS TIPO, \
                            A.TITULO, \
                            VARCHAR(SUBSTR(A.URL,1,1000)) AS URL, \
                            TP.ORDEN_TIPO \
                            FROM \
                            (SELECT * FROM CPD.TABLA \
                            WHERE VISIBLE=1 AND FECHA <= '{dia_ini}' AND FECHA >= '{dia_fin}' \
                            AND ID_TIPO IN (1,2) AND PERMANENTE = 0 \
                            AND (FECHA_VTO_PERM='1111-11-11' OR FECHA_VTO_PERM> CURRENT DATE ) ) AS A \
                            JOIN \
                            (SELECT * FROM CPD.TABLA2 WHERE ID_TIPO IN (1,2)) AS TP \
                            ON A.ID_TIPO = TP.ID_TIPO \
                            ORDER BY FECHA DESC, ORDEN_TIPO ASC, ID_NOVED DESC")
    else:
        
         sql_query = text(f"SELECT \
                            A.ID_NOVED, \
                            A.FECHA,  \
                            TP.NOMBRE AS TIPO, \
                            A.TITULO, \
                            VARCHAR(SUBSTR(A.URL,1,1000)) AS URL, \
                            TP.ORDEN_TIPO \
                            FROM \
                            (SELECT * FROM CPD.TABLA WHERE ID_TIPO IN (1,2) \
                            AND VISIBLE = 1 AND PERMANENTE <> 0 \
                            ORDER BY FECHA DESC, ID_NOVED DESC FETCH FIRST 5 ROWS ONLY \
                            ) AS A \
                            JOIN \
                            (SELECT * FROM CPD.TABLA2 WHERE ID_TIPO IN (1,2) ) AS TP \
                            ON A.ID_TIPO = TP.ID_TIPO \
                            UNION \
                            SELECT \
                            A.ID_NOVED, \
                            A.FECHA,  \
                            TP.NOMBRE AS TIPO, \
                            A.TITULO, \
                            VARCHAR(SUBSTR(A.URL,1,1000)) AS URL, \
                            TP.ORDEN_TIPO \
                            FROM \
                            (SELECT * FROM CPD.TABLA WHERE ID_TIPO IN (1,2) \
                            AND VISIBLE = 1 AND PERMANENTE = 0 \
                            AND (FECHA_VTO_PERM='1111-11-11' OR FECHA_VTO_PERM > CURRENT DATE) \
                            ) AS A \
                            JOIN \
                            (SELECT * FROM CPD.TABLA2 WHERE ID_TIPO IN (1,2) ) AS TP \
                            ON A.ID_TIPO = TP.ID_TIPO \
                            ORDER BY FECHA DESC,ORDEN_TIPO ASC,ID_NOVED DESC ")
        
    try:
        
        # Ejecutamos query y mapeamos
        result = db.execute(sql_query)
        normativa = mapea_resultado(result)

        
    except Exception as e : 
        print(f"Error al obtener fechas agrupadas de normativa: {e}")
        normativa = []

    return normativa
   