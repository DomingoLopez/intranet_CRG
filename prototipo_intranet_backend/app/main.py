from typing import Union
from fastapi import FastAPI


# Lanzar el server: uvicorn app.main:app --reload (para recargar ante cambios)
# python -m uvicorn app.main:app --reload ->>>>>>> Así es como se hace con el porculo de la versión 3.7.7
# Ver la ruta donde se genera la documentación. http://127.0.0.1:8000/docs (Hecho con swagger)
# Ver documentación alternativa: http://127.0.0.1:8000/redoc (Hecho con Redoc)
from app.app import create_app

app = create_app()
