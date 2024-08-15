from sqlalchemy import text
from sqlalchemy.orm import Session
from .mapeo import mapea_resultado

def get_hijos_db(db: Session):
    # Query definida
    try:
        sql_query = text("SELECT * FROM CPD.TD_MENU_CHILDS")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        hijos = mapea_resultado(result)
    except Exception as e : 
        print(f"Error al obtener tabla menu hijos: {e}")
        hijos = []

    return hijos