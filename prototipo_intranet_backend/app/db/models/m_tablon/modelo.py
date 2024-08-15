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

class Tablon:
    def __init__(self, id: int, canal:str, fecha: Date, tipo: str, categoria: str, titulo:str, url: Date, order: int):
        
        self.id = id
        self.canal = canal
        self.fecha = fecha
        self.tipo = tipo
        self.categoria = categoria
        self.titulo = titulo
        self.url = url 
        self.order = order
        
    def __str__(self):
        return f"ID: {self.id}, Canal: {self.canal}, Fecha: {self.fecha}, Tipo: {self.tipo}, Categoria: {self.categoria}, Titulo: {self.titulo}, Url: {self.url}"

    def __repr__(self):
        return f"Tablon(id={self.id}, canal={self.canal}, fecha={self.fecha}, tipo='{self.tipo}', categoria='{self.categoria}', titulo={self.titulo}', url={self.url}')"


    
    