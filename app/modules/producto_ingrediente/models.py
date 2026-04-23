from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import PrimaryKeyConstraint, Column, ForeignKey, Integer

if TYPE_CHECKING:
    from app.modules.producto.models import Producto
    from app.modules.ingrediente.models import Ingrediente

class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"

    # Clave primaria compuesta
    __table_args__ = (PrimaryKeyConstraint("producto_id", "ingrediente_id"),)

    producto_id: int = Field(sa_column=Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"), nullable=False))
    ingrediente_id: int = Field(sa_column=Column(Integer, ForeignKey("ingredientes.id", ondelete="CASCADE"), nullable=False))
    
    es_removible: bool = Field(default=False)

    # Relaciones directas
    producto: "Producto" = Relationship(back_populates="ingredientes_links")
    ingrediente: "Ingrediente" = Relationship(back_populates="productos_links")