from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import PrimaryKeyConstraint, Column, ForeignKey, Integer

if TYPE_CHECKING:
    from app.modules.producto.models import Producto
    from app.modules.categoria.models import Categoria

class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    # Clave primaria compuesta
    __table_args__ = (PrimaryKeyConstraint("producto_id", "categoria_id"),)

    producto_id: int = Field(sa_column=Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"), nullable=False))
    categoria_id: int = Field(sa_column=Column(Integer, ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False))
    
    es_principal: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relaciones directas 
    producto: "Producto" = Relationship(back_populates="categorias_links")
    categoria: "Categoria" = Relationship(back_populates="productos_links")