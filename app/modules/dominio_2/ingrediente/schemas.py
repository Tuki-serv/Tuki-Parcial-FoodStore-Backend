from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

# --- Esquemas auxiliares para las relaciones ---
class ProductoMin(BaseModel):
    id: int
    nombre: str

class IngredienteProductoLink(BaseModel):
    producto_id: int
    es_removible: bool
    producto: Optional[ProductoMin] = None


# --- Base y Entrada ---
class IngredienteBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: bool = False

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None


class IngredienteRead(IngredienteBase):
    id: int

class IngredienteList(SQLModel):
    data: List[IngredienteRead]
    total: int

class IngredienteFullRead(IngredienteRead):
    productos_links: List[IngredienteProductoLink] = []