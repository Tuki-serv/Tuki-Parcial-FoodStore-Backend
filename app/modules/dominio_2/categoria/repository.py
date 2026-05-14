from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from app.core.repository import BaseRepository
from app.modules.dominio_2.categoria.models import Categoria
from app.modules.dominio_2.producto_categoria.models import ProductoCategoria
from typing import Optional

class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Categoria)

    def get_by_id(self, record_id: int) -> Optional[Categoria]:
        statement = (
            select(Categoria)
            .where(Categoria.id == record_id)
            .options(
                selectinload(Categoria.parent),
                selectinload(Categoria.hijos),
                selectinload(Categoria.productos_links)
                .selectinload(ProductoCategoria.producto)
                )
        )
        return self.session.exec(statement).first()

    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        return self.session.exec(
            select(Categoria).where(Categoria.nombre == nombre)
        ).first()

    def get_active(self, offset: int = 0, limit: int = 20) -> list[Categoria]:
        return list(
            self.session.exec(
                select(Categoria)
                .where(Categoria.deleted_at.is_(None))
                .offset(offset)
                .limit(limit)
            ).all()
        )

    def count_active(self) -> int:
        return self.session.exec(
            select(func.count()).select_from(Categoria).where(Categoria.deleted_at.is_(None))
        ).one()