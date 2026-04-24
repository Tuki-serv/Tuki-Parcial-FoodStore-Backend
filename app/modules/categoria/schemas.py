from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel

# --- Esquemas auxiliares para las relaciones ---
class ProductoMin(BaseModel):
    id: int
    nombre: str
    precio_base: float

class CategoriaProductoLink(BaseModel):
    producto_id: int
    es_principal: bool
    producto: Optional[ProductoMin] = None

# --- Base y Entrada ---
class CategoriaBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None

# --- Salida ---
class CategoriaRead(CategoriaBase):
    id: int
    deleted_at : Optional[datetime]

class CategoriaList(SQLModel):
    """Respuesta paginada según el estándar de la unidad 4-actividad 1-endpoinds optimizados"""
    data: List[CategoriaRead]
    total: int

class CategoriaWithChildren(CategoriaRead):
    """Para mostrar el árbol en el Frontend"""
    parent: Optional["CategoriaRead"] = None
    hijos: List["CategoriaRead"] = []
    productos_links: List[CategoriaProductoLink] = []