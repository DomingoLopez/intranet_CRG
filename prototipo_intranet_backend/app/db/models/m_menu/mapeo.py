from .modelo import Menu

def mapea_resultado(result:any):
    
    menu = [Menu(
        id_menu=row[0],
        label=row[1],
        categoria=row[2],
        tipo_activo=row[3],
        url=row[4],
        order = 0,
        permitir_fav=True if row[5] == 'S' else False,
        ruta = row[6],
        is_fav=True if row[7] == 'S' else False
    ) for row in result.fetchall()]
    
    return menu

    

