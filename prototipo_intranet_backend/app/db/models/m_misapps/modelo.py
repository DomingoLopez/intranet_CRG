from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from app.db.session import Base
'''
Dado que el DB2 ha quedado obsoleto en cuanto a actualización de drivers y conexiones 
con frameworks modernos, hemos bajado a python 3.7.7 para que el conector funcione, pero 
no funciona el mapeo ORM por el tipo de dato que devuelve el DB2, por lo que 
simplemente usaremos SQLAlchemy para mapear con querys exactas de lo que necesitemos, 
definiendo los objetos necesarios. 

En este caso, esta es la clase para los objetos de tipo ACTIVO_INFORMACIÓN
'''

class MiAplicacion:
    def __init__(self, id: int, titulo: str, url: str):
        
        self.id = id
        self.titulo = titulo
        self.url = url 
        
    def __str__(self):
        return f"ID: {self.id}, Titulo: {self.titulo}, Url: {self.url}"

    def __repr__(self):
        return f"Normativa(id={self.id}, titulo={self.titulo}', url={self.url}')"


    
    