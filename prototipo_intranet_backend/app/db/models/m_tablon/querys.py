from sqlalchemy import text
from sqlalchemy.orm import Session
from .mapeo import mapea_resultado_db2, mapea_resultado_sharepoint
import requests as requests
from datetime import date, datetime, timedelta

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()
# Obtenemos las variables de entorno necesarias para hacer la llamada a sharepoint
SHAREPOINT_CLIENT_ID=os.getenv("SHAREPOINT_CLIENT_ID")
SHAREPOINT_TENANT_ID=os.getenv("SHAREPOINT_TENANT_ID")
SHAREPOINT_CLIENT_SECRET=os.getenv("SHAREPOINT_CLIENT_SECRET")


'''
Autenticación en Sharepoint
'''
def auth_sharepoint():

    # URL de autenticación en sharepoint
    url = f"https://accounts.accesscontrol.windows.net/{SHAREPOINT_TENANT_ID}/tokens/OAuth/2"
    # Parámetros que se enviarán en el cuerpo de la solicitud POST
    payload = {
        'grant_type': 'client_credentials',
        'client_id': f'{SHAREPOINT_CLIENT_ID}@{SHAREPOINT_TENANT_ID}',
        'client_secret': SHAREPOINT_CLIENT_SECRET,
        'resource' : f'xxxxxx/xxxxx.sharepoint.com@{SHAREPOINT_TENANT_ID}'
    }
    # Encabezados de la solicitud 
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # Realizar la solicitud POST
    response = requests.post(url, data=payload, headers=headers)
    return response
    


'''
Obtener las publicaciones sharepoint
'''
def get_publicaciones_sharepoint(token):

    publi_sharepoint = []
    # 2. Si token ok, hacemos otra petición al sharepoint para obtener la lista de publicaciones.    
    # 2.1. Obtener datos de sharepoint
    url ="https://xxxx.xxxx.com/sites/xxxx/_api/web/lists/getbytitle('CRG-Noticias%20publicadas%20CrgNet%2B')/items?&\$top=15&\$orderby=FechaModificacion%20desc"
    
    headers = {
    "Content-Type": "application/json",
    "Accept" :"application/json;odata=nometadata",
    "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    # Comprobamos 
    if response.status_code == 200:
        data = response.json()
        publi_sharepoint = data['value']
    else:
        print(f"Error al obtener publicaciones de sharepoint: {response.status_code}")
        print(response.text)
        return []
    
    # Añadimos valor de categoría a cada diccionario u objeto json
    tmp = [{**item, "categoria": "Sharepoint","tipo": "enlace"} for item in publi_sharepoint]
    # Mapeamos y creamos el array de objetivos publicación
    publicaciones_sharepoint = mapea_resultado_sharepoint(tmp)
    
    return publicaciones_sharepoint
    


def get_publicaciones_tablon(db: Session):
    
    # #############################################
    # 1ª Query para obtener las fechas de selección
    try:
        sql_query = text("SELECT FECHA      \
                            FROM CPD.TABLA    \
                            WHERE CPD.TABLA.VISIBLE=1     \
                            GROUP BY FECHA      \
                            ORDER BY FECHA DESC     \
                            FETCH FIRST 2 ROWS ONLY")
       # Intentamos ejecutar
        result = db.execute(sql_query)
        df = pd.DataFrame(result.fetchall(),columns=result.keys())

        # obtenemos días de los que obtener las publicaciones
        dia_uno = df.iloc[0, 0].strftime("%d/%m/%Y")
        dia_dos = df.iloc[1, 0].strftime("%d/%m/%Y")
       
    except Exception as e : 
        print(f"Error al obtener máxima y mínima de tablón: {e}")
        return []

    # #############################################
    # 2ª Query para obtener el tablón
    fecha_actual = date.today().strftime("%d/%m/%Y")
    if(fecha_actual == dia_uno):
        
        sql_query = text(f"SELECT   \
                            A.ID_NOVED, \
                            TP.NOMBRE, \
                            TO_CHAR(A.FECHA,'DD/MM/YYYY') AS FECHA,  \
                            CASE WHEN TP.NOMBRE = 'Portal Ciberseguridad' THEN 'enlace' ELSE 'archivo' END AS TIPO, \
                            'Tablon' AS CATEGORIA, \
                            A.TITULO, \
                            VARCHAR(SUBSTR(A.URL,1,1000)) AS URL \
                            FROM  \
                            (SELECT * FROM CPD.TABLA \
                            WHERE VISIBLE=1 \
                            AND (((FECHA = '{dia_uno}' OR FECHA = '{dia_dos}')\
                                AND  DAYS(CURRENT DATE)-DAYS (FECHA )<=3 ) OR (PERMANENTE=0 \
                                AND (FECHA_VTO_PERM='1111-11-11' OR FECHA_VTO_PERM> CURRENT DATE))) \
                            ) AS A \
                            JOIN \
                            (SELECT * FROM CPD.TABLA \
                            WHERE NOMBRE NOT IN ('Club Social','Club Esquí','Fundación') \
                            AND ID_TIPO NOT IN (1,2,6,10,11,12,13,24) \
                            ) AS TP \
                            ON A.ID_TIPO = TP.ID_TIPO")
    else:
        
         sql_query = text(f"SELECT  \
                            A.ID_NOVED, \
                            TP.NOMBRE, \
                            TO_CHAR(A.FECHA,'DD/MM/YYYY') AS FECHA, \
                            CASE WHEN TP.NOMBRE = 'Portal Ciberseguridad' THEN 'enlace' ELSE 'archivo' END AS TIPO, \
                            'Tablon' AS CATEGORIA, \
                            A.TITULO, \
                            VARCHAR(SUBSTR(A.URL,1,1000)) AS URL \
                            FROM  \
                            (SELECT * FROM CPD.TABLA \
                            WHERE VISIBLE=1 \
                                AND ((FECHA = '{dia_uno}'  \
                                AND DAYS(CURRENT DATE)-DAYS(FECHA)<=3 ) OR (PERMANENTE=0   \
                                AND (FECHA_VTO_PERM='1111-11-11' OR FECHA_VTO_PERM > CURRENT DATE))) \
                            ) AS A \
                            JOIN \
                            (SELECT * FROM CPD.TABLA \
                            WHERE NOMBRE NOT IN ('Club Social','Club Esquí','Fundación') \
                            AND ID_TIPO NOT IN (1,2,6,10,11,12,13,24) \
                            ) AS TP \
                            ON A.ID_TIPO = TP.ID_TIPO ")
    
    try:
       # Intentamos ejecutar
        result = db.execute(sql_query)
        publicaciones = mapea_resultado_db2(result)
    except Exception as e : 
        print(f"Error al obtener datos de tablón, sindical, etc: {e}")
        return []
    
    
    return publicaciones



    
'''
Función para ordenar y filtrar para quedarnos con los últimos 30 días de publicaciones:
- Ordenar for fecha modificación descendente
- Coger las publicaciones de los últimos 30 días.
- Coger aquellas publicaciones en función de los filtros que se conocen 
''' 
def filtrar_tablon(tablon):
    # --------------------------------
    # 1. Ordenar por fecha descendente
    tablon_sorted = sorted(tablon, key=lambda x: (datetime.strptime(x.fecha,'%d/%m/%Y')), reverse=True )
    # --------------------------------
    # 2. Filtrar por fecha de los últimos 30 días
    fecha_actual = datetime.now()
    # Calcular la fecha límite (hace 30 días)
    fecha_limite = fecha_actual - timedelta(days=30)
    # Convertir las fechas de los diccionarios y filtrar los que están en los últimos 30 días
    tablon_filter = [
        d for d in tablon_sorted 
        if datetime.strptime(d.fecha, '%d/%m/%Y') >= fecha_limite
    ]
    # --------------------------------
    # 3. Filtrar en función de los canales. 
    # Club social puede tener 3 publicaciones, 
    # el resto 2 publicaciones
    contador = {}
    tablon_final = []
    for item in tablon_filter:
        canal = item.canal
        if canal not in contador:
            contador[canal] = 1
            tablon_final.append(item)
        elif (canal == 'Club Social' and contador[canal] < 3) or contador[canal] < 2:
            contador[canal] += 1
            tablon_final.append(item)
    
    return tablon_final
    
        


'''
Obtenemos la normativa con los filtros indicados. 
'''
def get_tablon_db(db: Session):
    
    tablon = []
    # 1. obtener el token de acceso
    access_token = ""
    response_auth = auth_sharepoint()
    # Verificar que la solicitud fue exitosa
    if response_auth.status_code == 200:
        # Parsear la respuesta JSON
        data = response_auth.json()
        access_token = data['access_token']
    else:
        print(f"Error al obtener token de sharepoint: {response_auth.status_code}")
        print(response_auth.text)
        return []

    # Obtenemos ambos tipos de publicaciones (sharepoint online y tablón db2)
    publicaciones_sharepoint = get_publicaciones_sharepoint(access_token)
    publicaciones_tablon = get_publicaciones_tablon(db)
    # Juntamos ambos tipos de tablón
    tablon = publicaciones_sharepoint + publicaciones_tablon
    # Filtramos tablón con las casuísticas indicadas
    tablon_filtered = filtrar_tablon(tablon) 
   

    return tablon_filtered
    
    
 
    
    


   