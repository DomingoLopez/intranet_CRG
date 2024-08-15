from datetime import datetime
from .modelo import Tablon


def transformar_fecha(fecha_str):
    '''
    Función auxiliar para transformar el formato fecha que obtenemos
    de Sharepoint
    '''    
    # Parsear la fecha en formato ISO 8601 a un objeto datetime
    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%SZ")
    # Formatear el objeto datetime al formato deseado
    fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
    return fecha_formateada


def mapea_resultado_sharepoint(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    tablon = [Tablon(
        id = row['Id'],
        canal = row['Canal'],
        fecha = transformar_fecha(row['Modified']),
        tipo = row['tipo'].strip(),
        categoria = row['categoria'].strip(),
        titulo = row['Title'].strip(),
        url = row['Vinculo'],
        order = 0
    ) for row in result]

    return tablon




def mapea_resultado_db2(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    tablon = [Tablon(
        id = row[0],
        canal = row[1].strip(),
        fecha = row[2],
        tipo = row[3].strip(),
        categoria = row[4].strip(),
        titulo = row[5].strip(),
        url = row[6],
        order = 0
    ) for row in result.fetchall()]
 
    return tablon




