from sqlalchemy import text
from sqlalchemy.orm import Session
from .mapeo import mapea_resultado

def get_menu_db(db: Session):
    # Query definida
    try:
        sql_query = text(f"SELECT  \
                         A.ID_MENU,  \
                         A.LABEL, \
                         A.CATEGORIA, \
                         A.TIPO_ACTIVO, \
                         A.ENLACE,\
                         A.PERMITIR_FAV,\
                         A.RUTA, \
                         CASE WHEN B.ID_MENU IS NOT NULL THEN 'S' ELSE 'N' END AS IS_FAV \
                         FROM \
                         (SELECT * FROM CPD.TD_MENU_INTRANET) AS A \
                         LEFT OUTER JOIN \
                         (SELECT * FROM CPD.TD_FAV_MENU_USU WHERE ID_EMPLEADO = 'U971574') AS B \
                         ON A.ID_MENU = B.ID_MENU \
                         ")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        menu = mapea_resultado(result) 
    except Exception as e : 
        print(f"Error al obtener menu: {e}")
        menu = []

    return menu


def insertMenuFav(id_empleado:str, id_menu:int, db: Session):
    # Query definida
    try:
        sql_query = text(f"INSERT INTO CPD.TD_FAV_MENU_USU \
                         (ID_MENU, ID_EMPLEADO)   \
                         VALUES \
                         ({id_menu}, '{id_empleado}' )")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        db.commit()
    except Exception as e : 
        print(f"Error al insertar favorito menú: {e}")
        result = False

    return result


def deleteMenuFav(id_empleado:str, id_menu:int, db: Session):
    # Query definida
    try:
        sql_query = text(f"DELETE FROM CPD.TD_FAV_MENU_USU \
                         WHERE ID_MENU = {id_menu} AND ID_EMPLEADO = '{id_empleado}' \
                         ")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        db.commit()
    except Exception as e : 
        print(f"Error al borrar favorito menú: {e}")
        result = False
 
    return result