from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column, ARRAY, Text, Numeric

if TYPE_CHECKING:
    from app.modules.dominio_2.producto_categoria.models import ProductoCategoria
    from app.modules.dominio_2.producto_ingrediente.models import ProductoIngrediente

class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150, index=True)
    descripcion: Optional[str] = None
    
    # Manejo de array y decimal con SQLAlchemy puro dentro de SQLModel
    precio_base: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    imagenes_url: List[str] = Field(sa_column=Column(ARRAY(Text)), default=[])
    
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

    # Audit
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

    # Relaciones a las tablas intermedias
    categorias_links: List["ProductoCategoria"] = Relationship(back_populates="producto")
    ingredientes_links: List["ProductoIngrediente"] = Relationship(back_populates="producto")