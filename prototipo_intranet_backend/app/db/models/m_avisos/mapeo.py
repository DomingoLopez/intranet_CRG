from .modelo import Aviso

def mapea_resultado(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    avisos = [Aviso(
        id = row[0],
        centro = row[1],
        nomcentro =row[2].strip(),
        responsable_aviso = row[3].strip(),
        fecha = row[4],
        texto_aviso = row[5]
    ) for row in result.fetchall()]

    return avisos


