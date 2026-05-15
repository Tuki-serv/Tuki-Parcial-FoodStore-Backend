# Dominio 1
## usuarioModels
```
import uuid

from typing import Optional, List

from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship

from sqlalchemy import Column, CHAR

  

# ==========================================

# 1. TABLAS INTERMEDIAS (Link Models)

# ==========================================

  

class UsuarioRol(SQLModel, table=True):

    __tablename__ = "usuario_rol"

    # PK Compuesta

    usuario_id: uuid.UUID = Field(foreign_key="usuario.id", primary_key=True)

    rol_codigo: str = Field(foreign_key="rol.codigo", primary_key=True)

  

    # Atributos extra de la tabla intermedia según UML

    asignado_por_id: Optional[uuid.UUID] = Field(default=None, foreign_key="usuario.id")

    expires_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  

# ==========================================

# 2. TABLAS PRINCIPALES

# ==========================================

  

class Rol(SQLModel, table=True):

    __tablename__ = "rol"

    # PK Semántica (El ID es el texto "ADMIN", "CLIENT", etc.)

    codigo: str = Field(primary_key=True, max_length=20)

    nombre: str = Field(unique=True, index=True, max_length=50)

    descripcion: Optional[str] = None

    # Relaciones (N:M)

    usuarios: List["Usuario"] = Relationship(back_populates="roles", link_model=UsuarioRol)

  
  

class Usuario(SQLModel, table=True):

    __tablename__ = "usuario"

    # id: Optional[int] = Field(default=None, primary_key=True)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    nombre: str = Field(max_length=80)

    apellido: str = Field(max_length=80)

    email: str = Field(unique=True, index=True, max_length=254)

    celular: Optional[str] = Field(default=None, max_length=20)

    # Se fuerza el uso de CHAR(60) exacto para el hash de bcrypt

    password_hash: str = Field(sa_column=Column(CHAR(60), nullable=False))

  

    # Audit (Reemplaza a 'disabled')

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    deleted_at: Optional[datetime] = None

    # Relaciones

    roles: List[Rol] = Relationship(back_populates="usuarios", link_model=UsuarioRol)

    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="usuario")

    direcciones: List["DireccionEntrega"] = Relationship(back_populates="usuario")

  
  

# ==========================================

# 3. ENTIDADES ASOCIADAS (Dominio 1)

# ==========================================

  

class RefreshToken(SQLModel, table=True):

    __tablename__ = "refresh_token"

    id: Optional[int] = Field(default=None, primary_key=True)

  

    # usuario_id: int = Field(foreign_key="usuario.id")

    usuario_id: uuid.UUID = Field(foreign_key="usuario.id")

    token_hash: str = Field(sa_column=Column(CHAR(64), unique=True, nullable=False))

    expires_at: datetime

    revoked_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  

    usuario: Usuario = Relationship(back_populates="refresh_tokens")

  
  

class DireccionEntrega(SQLModel, table=True):

    __tablename__ = "direccion_entrega"

    id: Optional[int] = Field(default=None, primary_key=True)

    # usuario_id: int = Field(foreign_key="usuario.id")

    usuario_id: uuid.UUID = Field(foreign_key="usuario.id")

    alias: Optional[str] = Field(default=None, max_length=50)

    linea1: str

    linea2: Optional[str] = None

    ciudad: str = Field(max_length=100)

    provincia: Optional[str] = Field(default=None, max_length=100)

    codigo_postal: Optional[str] = Field(default=None, max_length=10)

    latitud: Optional[float] = None

    longitud: Optional[float] = None

    es_principal: bool = Field(default=False)

  

    # Audit

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    deleted_at: Optional[datetime] = None

  

    usuario: Usuario = Relationship(back_populates="direcciones")
```
## usuarioSchemas 

```
# --- Sub-Schemas para mostrar en la respuesta pública ---

class RolPublic(BaseModel):

    codigo: str

    nombre: str

    # descripcion: Optional[str] = None

  

# --- Entrada de datos (POST /register) ---

class UserCreate(BaseModel):

    nombre: str = Field(..., max_length=80)

    apellido: str = Field(..., max_length=80)

    email: EmailStr

    celular: Optional[str] = Field(default=None, max_length=20)

    password: str = Field(min_length=8)# poner limite

# --- Salida de datos (GET /me, Respuesta de Login/Register) ---

class UserPublic(BaseModel):

    id: uuid.UUID

    nombre: str

    apellido: str

    email: str

    celular: Optional[str] = None

    roles: List[RolPublic] = []

  

# --- Respuesta del Login ---

class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"

    expires_in: int
```

# Dominio 2
## categoria
### Models
```
from typing import TYPE_CHECKING, Optional

from app.modules.producto.models import ProductoCategoria
from ..base.models import BaseModel
from sqlmodel import Field, Relationship

# Evitar las importaciones circulares
if TYPE_CHECKING:
    from ..producto.models import Producto


class Categoria(BaseModel, table=True):
    __tablename__ = "categorias"
    
    parent_id: int | None = Field(
        default=None,
        foreign_key="categorias.id",
        description="FK a categoría padre"
    )
    
    nombre: str = Field(..., unique=True, max_length=100, description="Nombre de la categoría")
    
    descripcion: str | None = Field(default=None, description="Descripción")
    
    imagen_url: str = Field(..., description="URL de imagen de la categoría")

    parent: Optional["Categoria"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Categoria.id"}
    )
    
    children: list["Categoria"] = Relationship(
        back_populates="parent"
    )

    # Relación con productos a través de la tabla intermedia
    productos: list["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria
    )
```

### Schemas
```
from typing import Optional
from sqlmodel import Field, SQLModel


class ProductoBasicRead(SQLModel):
    id: int
    nombre: str


# ─── Base ─────────────────────────────────────────────────────────────────────────────────


class CategoriaBase(SQLModel):
    parent_id: Optional[int] = None
    nombre: str = Field(...,
                        description="Nombre de la categoría", max_length=100)
    descripcion: Optional[str] = Field(default=None, description="Descripción de la categoría")    
    imagen_url: str = Field(..., description="URL de imagen de la categoría")


# ─── Request schemas ──────────────────────────────────────────────────────────────────────
class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(SQLModel):
    parent_id: Optional[int] = None
    nombre: Optional[str] = Field(
        default=None, description="Nombre de la categoría", max_length=100)
    descripcion: Optional[str] = Field(
        default=None, description="Descripción de la categoría")
    imagen_url: Optional[str] = Field(
        default=None, description="URL de imagen de la categoría")


# ─── Response schemas ────────────────────────────────────────────────────────────────────


class CategoriaRead(CategoriaBase):
    id: int = Field(..., description="ID de la categoría")


class CategoriaReadSimple(CategoriaRead):
    """Categoría sin subcategorías - para listados"""
    pass


class CategoriaReadFull(CategoriaRead):
    productos: list[ProductoBasicRead] = Field(
        default_factory=list, description="Lista de productos")


#Se puede borrar? Revisar a lo ultimo
class CategoriaReadWithSubs(CategoriaRead):
    """Categoría con subcategorías - para árbol"""
    subcategorias: list[CategoriaReadSimple] = Field(
        default_factory=list,
        description="Subcategorías hijo"
    )


class CategoriaTreeNode(CategoriaRead):
    subcategorias: list["CategoriaTreeNode"] = Field(
        default_factory=list,
        description="Subcategorías anidadas"
    )


class CategoriaList(SQLModel):
    data: list[CategoriaReadFull]
    total: int


class CategoriaTreeList(SQLModel):
    data: list[CategoriaTreeNode]
    total: int


CategoriaTreeNode.model_rebuild()
```

## Ingredientes
### Models
```
from typing import TYPE_CHECKING
from ..base.models import BaseModel
from sqlmodel import Field, Relationship
from ..producto.models import ProductoIngrediente

if TYPE_CHECKING:
    from ..producto.models import Producto

class Ingrediente(BaseModel, table=True):
    __tablename__ = "ingredientes"
    nombre: str = Field(...,unique=True, description="Nombre del ingrediente")
    es_alergeno: bool = Field(default=False, description="Indica si el ingrediente es un alérgeno")
    descripcion: str | None = Field(default=None, description="Descripción del ingrediente")
    
    # Relación con productos a través de la tabla intermedia
    productos: list["Producto"] = Relationship(
        back_populates="ingredientes",
        link_model=ProductoIngrediente
    )
```
### Schemas
```
from typing import Optional
from sqlmodel import SQLModel, Field


# Esquema reducido local para evitar dependencia circular
class ProductoBasicRead(SQLModel):
    id: int
    nombre: str
# ─── Base ─────────────────────────────────────────────────────────────────────────────────


class IngredienteBase(SQLModel):
    nombre: str = Field(..., description="Nombre del ingrediente")
    es_alergeno: bool = Field(
        default=False, description="Indica si el ingrediente es un alérgeno")
    descripcion: Optional[str] = Field(default=None, description="Descripción del ingrediente")


# ─── Request schemas ──────────────────────────────────────────────────────────────────────


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = Field(
        default=None, description="Nombre del ingrediente")
    es_alergeno: Optional[bool] = Field(
        default=None, description="Indica si el ingrediente es un alérgeno")
    descripcion: Optional[str] = Field(
        default=None, description="Descripción del ingrediente")


# ─── Response schemas ────────────────────────────────────────────────────────────────────

class IngredienteRead(IngredienteBase):
    id: int = Field(..., description="ID del ingrediente")


class IngredienteBasicRead(SQLModel):
    id: int = Field(..., description="ID del ingrediente")
    nombre: str = Field(..., description="Nombre del ingrediente")


class IngredienteReadFull(IngredienteRead):
    productos: list[ProductoBasicRead] = Field(
        default_factory=list, description="Lista de productos")


class IngredienteList(SQLModel):
    data: list[IngredienteReadFull]
    total: int
```

## Productos
### Models
```
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from pydantic import field_validator
from ..base.models import BaseModel
from sqlmodel import Field, Relationship, Column, Integer, ForeignKey, SQLModel, ARRAY, String
from sqlalchemy import CheckConstraint, Numeric


if TYPE_CHECKING:
    from ..categoria.models import Categoria
    from ..ingrediente.models import Ingrediente


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"
    
    # La combinación de producto_id y categoria_id para evitar duplicados de relacion
    producto_id: int = Field(
        sa_column=Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"),  #borra relaciones si se borra el producto
        primary_key=True, nullable=False)
    )
    categoria_id: int = Field(
        sa_column=Column(Integer, ForeignKey("categorias.id", ondelete="RESTRICT"), #no permite borrar categoria si tiene productos relacionados
        primary_key=True, nullable=False)
    )
    es_principal: bool = Field(default=False, description="Indica si es categoría principal del producto")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"
    
    producto_id: int = Field(
        sa_column=Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"), 
        primary_key=True, nullable=False)
    )
    ingrediente_id: int = Field(
        sa_column=Column(Integer, ForeignKey("ingredientes.id", ondelete="RESTRICT"), 
        primary_key=True, nullable=False)
    )
    es_removible: bool = Field(default=False, description="Indica si el ingrediente es removible")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class Producto(BaseModel, table=True):
    __tablename__ = "productos"

    # Constraint a nivel de BD: última línea de defensa
    __table_args__ = (
        CheckConstraint("precio_base >= 0", name="ck_producto_precio_no_negativo"),
    )

    #no puede ser nulo
    nombre: str = Field(..., description="Nombre del producto", max_length=150)
    descripcion: Optional[str] = Field(default=None, description="Descripción del producto")
    #no puede ser nulo y checar que sea mayor o igual a 0
    precio_base: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False),
        description="Precio base del producto"
    )
    imagenes_url: Optional[list[str]] = Field(default=None, sa_column=Column(ARRAY(String)))    
    stock_cantidad: int = Field(default=0, ge=0, description="Cantidad en stock")
    disponible: bool = Field(default=True, description="Si el producto está disponible para venta")
    
    # ── Validador de dominio (capa Python) ────────────────────────────────
    @field_validator("precio_base")
    @classmethod
    def precio_no_negativo(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("El precio base no puede ser negativo")
        return v

    # Relaciones N:N Bidireccional
    categorias: list["Categoria"] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoria
    )
    ingredientes: list["Ingrediente"] = Relationship(
        back_populates="productos",
        link_model=ProductoIngrediente
    )
```

### Schemas
```
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


class CategoriaBasicRead(SQLModel):
    id: int
    nombre: str
    es_principal: bool = Field(
        default=False, description="Si es categoría principal")


class IngredienteBasicRead(SQLModel):
    id: int
    nombre: str
    es_alergeno: bool = Field(default=False, description="Si es alérgeno")


# ─── Base ─────────────────────────────────────────────────────────────────────────────────


class ProductoBase(SQLModel):
    nombre: str = Field(..., description="Nombre del producto", max_length=150)
    descripcion: Optional[str] = Field(
        default=None, description="Descripción del producto")
    precio_base: Decimal = Field(..., description="Precio del producto", ge=0)
    imagenes_url: Optional[list[str]] = Field(
        default=None, description="URLs de imágenes del producto")
    stock_cantidad: int = Field(
        default=0, ge=0, description="Cantidad en stock")
    disponible: bool = Field(
        default=True, description="Indica si el producto está disponible")

# ─── Request schemas ──────────────────────────────────────────────────────────────────────


class ProductoCreate(ProductoBase):
    categoria_ids: list[int] = Field(
        ..., 
        min_length=1, 
        description="Lista de IDs de categorías a las que pertenece (obligatorio, mínimo 1)"
    )
    ingrediente_ids: Optional[list[int]] = Field(
        default=None, 
        description="Lista opcional de IDs de ingredientes"
    )


class ProductoUpdate(SQLModel):
    nombre: Optional[str] = Field(
        default=None, description="Nombre del producto", max_length=150)
    descripcion: Optional[str] = Field(
        default=None, description="Descripción del producto")
    precio_base: Optional[Decimal] = Field(
        default=None, description="Precio del producto", ge=0)
    imagenes_url: Optional[list[str]] = Field(
        default=None, description="URLs de imágenes del producto")
    stock_cantidad: Optional[int] = Field(
        default=None, description="Cantidad en stock", ge=0)
    disponible: Optional[bool] = Field(
        default=None, description="Indica si el producto está disponible")
    categoria_ids: Optional[list[int]] = Field(
        default=None, min_length=1, description="Lista opcional de IDs de categorías para actualizar"
    )
    ingrediente_ids: Optional[list[int]] = Field(
        default=None, description="Lista opcional de IDs de ingredientes para actualizar"
    )

# ─── Response schemas ────────────────────────────────────────────────────────────────────


class ProductoRead(ProductoBase):
    id: int = Field(..., description="ID del producto")


class ProductoBasicRead(SQLModel):
    id: int = Field(..., description="ID del producto")
    nombre: str = Field(..., description="Nombre del producto")
    precio_base: Decimal = Field(..., description="Precio del producto", ge=0)
    imagenes_url: Optional[list[str]] = Field(
        default=None, description="URLs de imágenes del producto")


class ProductoReadFull(ProductoRead):
    """Producto con categorías e ingredientes"""
    categorias: list[CategoriaBasicRead] = Field(default_factory=list)
    ingredientes: list[IngredienteBasicRead] = Field(default_factory=list)


# Facilita al frontend obtener el total de productos
# para paginación sin hacer una consulta extra
class ProductoList(SQLModel):
    data: list[ProductoReadFull]
    total: int = Field(..., description="Total de productos disponibles")
```
# Dominio 3