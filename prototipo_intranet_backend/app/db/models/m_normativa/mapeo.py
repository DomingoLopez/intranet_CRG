from datetime import datetime
from .modelo import Normativa

def mapea_resultado(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    normativa = [Normativa(
        id = row[0],
        fecha = row[1].strftime("%d/%m/%Y"),
        tipo = row[2].strip(),
        titulo = row[3].strip(),
        url = row[4].strip(),
        order = row[5]
    ) for row in result.fetchall()]

    return normativa


