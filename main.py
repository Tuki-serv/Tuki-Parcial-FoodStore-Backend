from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine

from app.modules.dominio_2.categoria.router import router as categoria_router
from app.modules.dominio_2.producto.router import router as producto_router
from app.modules.dominio_2.ingrediente.router import router as ingrediente_router
from app.modules.dominio_1.usuario.routers import router as usuario_router

from app.utils.errores import manejar_http_exceptions, manejar_validaciones

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="Tuki-FoodStore API",
        description="Parcial Programación IV - Implementación Profesional de Relaciones Complejas",
        version="1.0.0",
        lifespan=lifespan
    )

    origenes_permitidos = [
        "http://localhost:5173",  # Puerto por defecto de Vite (React)
        "http://localhost:3000",  # Puerto por defecto de Create React App
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origenes_permitidos, # URLs permitidas
        allow_credentials=True,
        allow_methods=["*"], # Permite todos los métodos HTTP
        allow_headers=["*"], # Permite todos los headers
    )

    
    app.include_router(categoria_router)
    app.include_router(producto_router)
    app.include_router(ingrediente_router)
    app.include_router(usuario_router)

    app.add_exception_handler(HTTPException, manejar_http_exceptions)
    app.add_exception_handler(RequestValidationError, manejar_validaciones)

    return app

app = create_app()