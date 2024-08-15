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

class Autorizacion:
    def __init__(self, num_empleado: int, programa: str, autorizacion: str):
        self.num_empleado = num_empleado
        self.programa = programa
        self.autorizacion = autorizacion

        
    def __str__(self):
        return f"Empleado: {self.num_empleado}, Programa: {self.programa}, Autorizacion: {self.autorizacion}"

    def __repr__(self):
        return f"Autorizacion(num_empleado={self.num_empleado}, programa={self.programa}, autorizacion='{self.autorizacion}')"


    
    