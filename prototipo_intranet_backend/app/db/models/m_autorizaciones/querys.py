from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.models.request.auth_program_data import AuthProgramData
from .mapeo import mapea_resultado


def get_autorizaciones(auth_program_data: AuthProgramData, db: Session):
    
    user = auth_program_data.num_empleado
    program = auth_program_data.program
    
    # Query definida
    try:
        sql_query = text(f"SELECT \
                            NUM_EMPLEADO,       \
                            PROGRAMA_WEBFOCUS,     \
                            AUTORIZ \
                            FROM CPD.TABLA \
                            WHERE NUM_EMPLEADO = '{user}' AND PROGRAMA_WEBFOCUS = '{program}';")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        autorizacion = mapea_resultado(result)
    except Exception as e : 
        print(f"Error al obtener avisos: {e}")
        autorizacion = None

    return autorizacion
