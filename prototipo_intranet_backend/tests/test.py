# Pruebas varias

# Imports de fastApi
import sys
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Body

from sqlalchemy import text
from sqlalchemy.orm import Session

# Importaciones para que reconozca la ruta de los módulos
import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Obtener la ruta del directorio actual del script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Agregar el directorio padre al sys.path
parent_directory = os.path.abspath(os.path.join(current_directory, '../..'))
sys.path.append(parent_directory)

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String

from ldap3 import Server, Connection, ALL, NTLM

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Ahora puedes acceder a las variables de entorno cargadas
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_USER=os.getenv("DB_USER")
DB_PASSWD=os.getenv("DB_PASSWD")

SQLALCHEMY_DATABASE_URL = f'ibm_db_sa://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/INSTANCIA'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependencia de sesion de la BBDD, estoy hay que ponerlo fuera, aqui no pinta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def mapea_resultado_menu(result:any):
    # Extraer valores de cada fila y crear instancias de Empleado
    menu = [Menu(
        id_menu=row[0],
        label=row[1],
        categoria=row[2],
        tipo_activo=row[3],
        enlace=row[4],
        order = 0,
        permitir_fav=row[5],
        ruta = row[6]
    ) for row in result.fetchall()]
    
    return menu
        
        
def mapea_resultado_child(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    childs = [Child(
        id_menu=row[0],
        id_child=row[1],
        order=row[2]
    ) for row in result.fetchall()]
    
    return childs
        
        
        

class Menu:
    '''
    Dado que el DB2 ha quedado obsoleto en cuanto a actualizacion de drivers y conexiones 
    con frameworks modernos, hemos bajado a python 3.7.7 para que el conector funcione, pero 
    no funciona el mapeo ORM por el tipo de dato que devuelve el DB2, por lo que 
    simplemente usaremos SQLAlchemy para mapear con querys exactas de lo que necesitemos, 
    definiendo los objetos necesarios. 

    En este caso, esta es la clase para los objetos de tipo ACTIVO_INFORMACIoN
    '''    
    def __init__(self, id_menu: int, label: str, categoria: str, tipo_activo: str, url: str, order:int, permitir_fav: bool, is_fav: bool, ruta:str, childs: None = []):
        self.id_menu = id_menu
        self.label = label
        self.categoria = categoria
        self.tipo_activo = tipo_activo
        self.url = url
        self.order = order 
        self.permitir_fav = permitir_fav
        self.is_fav = is_fav
        self.ruta = ruta
        self.childs = childs

    def __str__(self):
        return (f"ID: {self.id_menu}, Label: {self.label}, Categoria: {self.categoria}, Tipo de Activo: {self.tipo_activo}, "
                f"Enlace: {self.url}, Orden: {self.order}, Permitir Favorito: {self.permitir_fav}, Es Favorito: {self.is_fav}, Ruta: {self.ruta}, Hijos: {self.childs}")

    def __repr__(self):
        return (f"Menu(id_menu={self.id_menu}, label='{self.label}', categoria='{self.categoria}', tipo_activo='{self.tipo_activo}', "
                f"url='{self.url}', order={self.order}, permitir_fav={self.permitir_fav}, es_fav={self.is_fav}, ruta={self.ruta}, childs={self.childs})")


class Child:
    '''
    Dado que el DB2 ha quedado obsoleto en cuanto a actualizacion de drivers y conexiones 
    con frameworks modernos, hemos bajado a python 3.7.7 para que el conector funcione, pero 
    no funciona el mapeo ORM por el tipo de dato que devuelve el DB2, por lo que 
    simplemente usaremos SQLAlchemy para mapear con querys exactas de lo que necesitemos, 
    definiendo los objetos necesarios. 

    En este caso, esta es la clase para los objetos de tipo ACTIVO_INFORMACIoN
    '''
    def __init__(self, id_menu: int, id_child: int, order: int):
        self.id_menu = id_menu
        self.id_child = id_child
        self.order = order

    def __str__(self):
        return f"ID del Menú: {self.id_menu}, ID del Hijo: {self.id_child}, Orden: {self.order}"

    def __repr__(self):
        return f"Child(id_menu={self.id_menu}, id_child={self.id_child}, order={self.order})"

def mapea_resultado_menu(result:any):
    
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
        menu = mapea_resultado_menu(result)
    except Exception as e : 
        print(f"Error al obtener menu: {e}")
        menu = []

    return menu


def mapea_resultado_hijos(result: any):
    # Extraer valores de cada fila y crear instancias de Child
    childs = [Child(
        id_menu=row[0],
        id_child=row[1],
        order=row[2]
    ) for row in result.fetchall()]
    
    return childs

def get_hijos_db(db: Session):
    # Query definida
    try:
        sql_query = text("SELECT * FROM CPD.TD_MENU_CHILDS")
        # Intentamos ejecutar
        result = db.execute(sql_query)
        hijos = mapea_resultado_hijos(result)
    except Exception as e : 
        print(f"Error al obtener tabla menu hijos: {e}")
        hijos = []

    return hijos



from pydantic import BaseModel

class User(BaseModel): 
    
    _id: str
    id_empleado: str
    centro: str
    nomcentro: str
    nombre: str
    isActive: bool
    roles: list
    

def map_ldap_to_user(entry):
    user = User(
        _id=str(entry.entry_dn),
        id_empleado=entry.sAMAccountName.value,
        centro=entry.departmentNumber.value if entry.departmentNumber else '',
        nomcentro=entry.department.value if entry.department else '',
        nombre=entry.displayName.value if entry.displayName else '',
        isActive=True if entry.accountExpires and entry.accountExpires.value == '9999-12-31 22:59:59+00:00' else False,
        roles=[]  # Puedes agregar lógica para mapear roles si es necesario
    )
    return user


if __name__ == "__main__":


    # Configuración del servidor y la conexión
    server_address = 'ldap://ADCONNECTDOMINIO'
    username = 'DOMINIO\\USER'
    password = 'PASS'
    search_base = 'OU=OU,DC=DOMINIO,DC=com'

    # Establecer conexión con el servidor LDAP
    server = Server(server_address, get_info=ALL)
    conn = Connection(server, user=username, password=password, authentication=NTLM, auto_bind=False)

    if conn.bind():
        print("Autenticación exitosa")
    else:
        print("Autenticación fallida")
        print("Error:", conn.result['description'])

    # Realizar la búsqueda
    search_filter = '(samaccountname=U971574)'
    search_attributes = ['samaccountname', 'departmentnumber', 'department', 'displayname', 'accountexpires']

    # Ejecutar la búsqueda en el Directorio Activo
    conn.search(search_base, search_filter, attributes=search_attributes)

    # Obtener y mostrar los resultados
    if conn.entries:
        user = map_ldap_to_user(conn.entries[0])
        print(user)


    else:
        print('No se encontró ningún usuario con employeeNumber = 1574')

    # Cerrar la conexión
    conn.unbind()





