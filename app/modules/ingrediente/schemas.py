from typing import Optional, List
from sqlmodel import SQLModel, Field

class IngredienteBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: bool = False

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None

class IngredienteRead(IngredienteBase):
    id: int

class IngredienteList(SQLModel):
    data: List[IngredienteRead]
    total: int