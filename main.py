from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlmodel import SQLModel

from app.core.database import engine

from app.modules.categoria.router import router as categoria_router
from app.modules.producto.router import router as producto_router
from app.modules.ingrediente.router import router as ingrediente_router

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

    
    app.include_router(categoria_router)
    app.include_router(producto_router)
    app.include_router(ingrediente_router)

    app.add_exception_handler(HTTPException, manejar_http_exceptions)
    app.add_exception_handler(RequestValidationError, manejar_validaciones)

    return app

app = create_app()