from dotenv import load_dotenv
from ldap3 import Server, Connection, ALL, NTLM
from datetime import datetime, timezone
import os

from app.core.models.user import User
# Carga las variables de entorno desde el archivo .env
load_dotenv()

USER_AD=os.getenv("USERAD")
PASS_AD=os.getenv("PASSAD")
HOST_AD=os.getenv("HOST_AD")
DOMAIN_AD=os.getenv("DOMAIN_AD")



def get_conn_AD(user=USER_AD, passwd=PASS_AD):
    '''
    Función para conectar con AD
    '''    
    # Establecemos variables
    server_address = f'ldap://{HOST_AD}'
    username = f'{DOMAIN_AD}\\{user}'
    password = passwd
    # Establecer conexión con el servidor LDAP
    server = Server(server_address, get_info=ALL)
    conn = Connection(server, user=username, password=password, authentication=NTLM, auto_bind=False)

    return conn



def close_AD_conn(conn: Connection):
    '''
    Función para cerrar una conexión existente
    '''
    conn.unbind()




def map_ldap_to_user(entry):
    '''
    Mapear un usuario de AD
    '''
    account_expires = entry.accountExpires.value if entry.accountExpires else datetime.max.replace(tzinfo=timezone.utc)
    is_active = datetime.now(timezone.utc) <= account_expires
    
    if not is_active:
        return False
    else:
        user = User(
            _id=str(entry.entry_dn),
            id_empleado=entry.sAMAccountName.value,
            centro=entry.departmentNumber.value if entry.departmentNumber else '',
            nomcentro=entry.department.value if entry.department else '',
            nombre=entry.displayName.value if entry.displayName else '',
            isActive=is_active,
            roles=[]  # Puedes agregar lógica para mapear roles si es necesario
        )
        return user



'''
Función para autenticar en AD
con un usuario y contraseña dados
'''
def auth_AD(user, password):
    # Obtenemos conexión
    conn = get_conn_AD(user, password)
    # Comprobamos si todo ha ido bien
    if conn.bind():
        # Si todo bien, recuperamos y devolvemos el usuario
        search_base = f'OU=GRUPO,DC={DOMAIN_AD},DC=com'
        search_filter = f'(samaccountname={user})'
        search_attributes = ['samaccountname', 'departmentnumber', 'department', 'displayname', 'accountexpires']
        # Ejecutar la búsqueda en el Directorio Activo
        conn.search(search_base, search_filter, attributes=search_attributes)
        # Obtener y mostrar los resultados
        if conn.entries:
            user = map_ldap_to_user(conn.entries[0])
        else:
            print(f'No se encontró ningún usuario con samaccountname = {user}')
            
        close_AD_conn(conn)
        return user
    else:
        return False