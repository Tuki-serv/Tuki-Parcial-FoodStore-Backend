from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime

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
    hijos: List["CategoriaRead"] = []