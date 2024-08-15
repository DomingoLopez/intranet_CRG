from sqlalchemy import text
from sqlalchemy.orm import Session
from .mapeo import mapea_resultado

# TODO: Hay que hacer algo con el usuario, ya que dependiendo de 
# OFIC_SSCC O la variable DESTINO, salen unas cosas u otras.
def get_avisos_db(db: Session):
    # Query definida
    try:
        sql_query = text("SELECT \
                            ID_AVISO,       \
                            CENTRO_SOL,     \
                            NOMCENTRO_SOL,  \
                            RESPONSABLE_AVISO, \
                            TO_CHAR(FECHA,'dd/MM/YYYY') AS FECHA, \
                            TEXTO_AVISO \
                            FROM CPD.TABLA \
                            WHERE CANAL_AVISO_CI ='S' AND VISIBLE_AVISO_CI='S' \
                            AND FECHA > CURRENT DATE - 5 DAYS AND (DESTINO='EMPRESA' OR DESTINO='OFIC_SSCC') ORDER BY FECHA DESC,ID_AVISO DESC;")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        avisos = mapea_resultado(result)
    except Exception as e : 
        print(f"Error al obtener avisos: {e}")
        avisos = []

    return avisos
