from .modelo import Child

def mapea_resultado(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    childs = [Child(
        id_menu=row[0],
        id_child=row[1],
        order=row[2]
    ) for row in result.fetchall()]
    
    return childs


