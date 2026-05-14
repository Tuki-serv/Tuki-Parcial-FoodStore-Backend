from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.dominio_2.producto_categoria.models import ProductoCategoria

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Auto-referencia para subcategorías (0..1 a parent)
    parent_id: Optional[int] = Field(default=None, foreign_key="categorias.id")
    
    nombre: str = Field(max_length=100, unique=True, index=True)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

    # Audit
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

    # Relaciones auto-referenciales
    # Con esto creo una lista de adyacencia ajjajaajja
    parent: Optional["Categoria"] = Relationship(
        back_populates="hijos",
        sa_relationship_kwargs={"remote_side": "Categoria.id"}
    )
    hijos: List["Categoria"] = Relationship(back_populates="parent")

    # Relación a la tabla intermedia
    productos_links: List["ProductoCategoria"] = Relationship(back_populates="categoria")