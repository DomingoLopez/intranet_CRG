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
class Child:
    def __init__(self, id_menu: int, id_child: int, order: int):
        self.id_menu = id_menu
        self.id_child = id_child
        self.order = order

    def __str__(self):
        return f"ID del Menú: {self.id_menu}, ID del Hijo: {self.id_child}, Orden: {self.order}"

    def __repr__(self):
        return f"Child(id_menu={self.id_menu}, id_child={self.id_child}, order={self.order})"



    
    