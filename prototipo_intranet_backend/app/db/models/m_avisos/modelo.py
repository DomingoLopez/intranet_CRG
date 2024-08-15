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

class Aviso:
    def __init__(self, id: int, centro: int, nomcentro: str, responsable_aviso:str, fecha: Date, texto_aviso: str):
        self.id = id
        self.centro = centro
        self.nomcentro = nomcentro
        self.responsable_aviso = responsable_aviso
        self.fecha = fecha
        self.texto_aviso = texto_aviso
        
    def __str__(self):
        return f"ID: {self.id}, Centro: {self.centro}, Nombre del Centro: {self.nomcentro}, Responsable aviso: {self.responsable_aviso}, Fecha: {self.fecha}, Texto del Aviso: {self.texto_aviso}"

    def __repr__(self):
        return f"Aviso(id={self.id}, centro={self.centro}, nomcentro='{self.nomcentro}', responsable_aviso={self.responsable_aviso}', fecha={self.fecha}, texto_aviso='{self.texto_aviso}')"


    
    