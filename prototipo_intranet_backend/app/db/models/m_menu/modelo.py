from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
'''
Dado que el DB2 ha quedado obsoleto en cuanto a actualización de drivers y conexiones 
con frameworks modernos, hemos bajado a python 3.7.7 para que el conector funcione, pero 
no funciona el mapeo ORM por el tipo de dato que devuelve el DB2, por lo que 
simplemente usaremos SQLAlchemy para mapear con querys exactas de lo que necesitemos, 
definiendo los objetos necesarios. 

En este caso, esta es la clase para los objetos de tipo ACTIVO_INFORMACIÓN
'''
class Menu:
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