from .modelo import MiAplicacion

def mapea_resultado(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    misapps = [MiAplicacion(
        id = row[0],
        titulo = row[1].strip(),
        url = row[2].strip()
    ) for row in result.fetchall()]

    return misapps


