from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import menu
from app.routers import avisos
from app.routers import normativa
from app.routers import mis_aplicaciones
from app.routers import tablon
from app.routers import menu_fav
from app.routers.auth import auth
from app.routers.auth_programs import autorizaciones


def create_app() -> FastAPI:
    app = FastAPI(title="Prototipo Intranet")

    # Incluímos las rutas necesarias del aplicativo
    app.include_router(menu.router)
    app.include_router(avisos.router)
    app.include_router(normativa.router)
    app.include_router(mis_aplicaciones.router)
    app.include_router(tablon.router)
    app.include_router(menu_fav.router)
    # Incluir las rutas de autenticación
    app.include_router(auth.router)
    # Incluir las rutas de autenticación en programas 
    app.include_router(autorizaciones.router)

    # For local development
    origins = [
        "http://localhost:3000",
        "http://localhost:4200",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Generic health route to sanity check the API
    @app.get("/health")
    async def health() -> str:
        return "ok"

    return app