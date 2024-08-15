import sqlalchemy
from sqlalchemy import *
import ibm_db_sa
import os
import ibm_db
import ibm_db_dbi

# Ahora puedes acceder a las variables de entorno cargadas
DB_HOST='XXXXXXXXX'
DB_PORT='XXXXX'
DB_USER='XXXX'
DB_PASSWD='XXXX'


db2 = sqlalchemy.create_engine(f'ibm_db_sa://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/INSTANCIA')


# Definir la tabla
metadata = MetaData()
users = Table('CPD.TABLA', metadata)

try:
    with db2.connect() as conn:
        print("OK")

        # Ejecutar una consulta
        query = text("SELECT * FROM CPD.TABLA")  # Pasamos solo la columna ID_EMPLEADO
        result = conn.execute(query)

        # Obtener los resultados
        rows = result.fetchall()
        for row in rows:
            print(row)
except Exception as e:
    print("MAL", e)