from .modelo import Autorizacion

def mapea_resultado(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    autorizacion = [Autorizacion(
        num_empleado = row[0],
        programa = row[1],
        autorizacion =row[2]
    ) for row in result.fetchall()]

    return autorizacion


