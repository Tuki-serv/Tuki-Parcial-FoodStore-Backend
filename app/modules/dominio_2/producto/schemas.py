from typing import Optional, List
from decimal import Decimal
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

from app.modules.dominio_2.categoria.schemas import CategoriaRead
from app.modules.dominio_2.ingrediente.schemas import IngredienteRead

# --- Esquemas para los "Links" (Tablas intermedias) ---
class ProductoIngredienteRead(BaseModel):
    ingrediente_id: int
    es_removible: bool
    # Agregamos la relación para ver el nombre y descripción del ingrediente
    ingrediente: Optional[IngredienteRead] = None 

    class Config:
        from_attributes = True

class ProductoCategoriaRead(BaseModel):
    categoria_id: int
    es_principal: bool
    # Agregamos la relación para ver el nombre de la categoría
    categoria: Optional[CategoriaRead] = None

    class Config:
        from_attributes = True

# --- Producto principal ---
class ProductoBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Decimal
    imagenes_url: List[str] = []
    stock_cantidad: int = 0
    disponible: bool = True

class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = []
    ingrediente_ids: List[int] = []

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=150)
    precio_base: Optional[Decimal] = Field(default=None, ge=0)
    stock_cantidad: Optional[int] = Field(default=None, ge=0)
    disponible: Optional[bool] = None

class ProductoRead(ProductoBase):
    id: int

class ProductoList(SQLModel):
    data: List[ProductoRead]
    total: int

class ProductoFullRead(ProductoRead):
    """
    Respuesta completa con relaciones para el detalle del producto.    """
    categorias_links: List[ProductoCategoriaRead] = []
    ingredientes_links: List[ProductoIngredienteRead] = []