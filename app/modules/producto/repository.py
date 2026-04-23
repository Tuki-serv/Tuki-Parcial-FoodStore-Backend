from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from app.core.repository import BaseRepository
from app.modules.producto.models import Producto
from app.modules.producto_categoria.models import ProductoCategoria
from app.modules.producto_ingrediente.models import ProductoIngrediente
from typing import Optional

class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Producto)

    def get_by_id(self, record_id: int) -> Optional[Producto]:
        statement = (
            select(Producto)
            .where(Producto.id == record_id)
            .options(
                selectinload(Producto.categorias_links).selectinload(ProductoCategoria.categoria),
                selectinload(Producto.ingredientes_links).selectinload(ProductoIngrediente.ingrediente)
            )
        )
        return self.session.exec(statement).first()

    def get_by_nombre(self, nombre: str) -> Optional[Producto]:
        return self.session.exec(
            select(Producto).where(Producto.nombre == nombre)
        ).first()

    def get_active(self, offset: int = 0, limit: int = 20,categoria_id: Optional[list[int]] = None,ingrediente_id: Optional[list[int]] = None) -> list[Producto]:
        query = select(Producto).where(Producto.deleted_at.is_(None))
        if categoria_id:
            query = query.join(ProductoCategoria).where(ProductoCategoria.categoria_id.in_(categoria_id))
        if ingrediente_id:
            query = query.join(ProductoIngrediente).where(ProductoIngrediente.ingrediente_id.in_(ingrediente_id))
        return list(self.session.exec(query.offset(offset).limit(limit)).all())


    def count_active(self,categoria_id: Optional[list[int]] = None,ingrediente_id: Optional[list[int]] = None) -> int:
        query = select(func.count()).select_from(Producto).where(Producto.deleted_at.is_(None))
        if categoria_id:
            query = query.join(ProductoCategoria).where(ProductoCategoria.categoria_id.in_(categoria_id))
        if ingrediente_id:
            query = query.join(ProductoIngrediente).where(ProductoIngrediente.ingrediente_id.in_(ingrediente_id))
        return self.session.exec(query).one()