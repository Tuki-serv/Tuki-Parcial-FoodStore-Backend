from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from app.core.repository import BaseRepository
from app.modules.dominio_2.ingrediente.models import Ingrediente
from app.modules.dominio_2.producto_ingrediente.models import ProductoIngrediente
from typing import Optional

class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Ingrediente)

    def get_by_id(self, record_id: int) -> Optional[Ingrediente]:
        statement = (
            select(Ingrediente)
            .where(Ingrediente.id == record_id)
            .options(
                selectinload(Ingrediente.productos_links)
                .selectinload(ProductoIngrediente.producto)
                )
        )
        return self.session.exec(statement).first()

    def get_by_nombre(self, nombre: str) -> Optional[Ingrediente]:
        return self.session.exec(
            select(Ingrediente).where(Ingrediente.nombre == nombre)
        ).first()

    def get_active(self, offset: int = 0, limit: int = 20) -> list[Ingrediente]:
        return list(
            self.session.exec(
                select(Ingrediente)
                .where(Ingrediente.deleted_at.is_(None))
                .offset(offset)
                .limit(limit)
            ).all()
        )

    def count_active(self) -> int:
        return self.session.exec(
            select(func.count())
            .select_from(Ingrediente)
            .where(Ingrediente.deleted_at.is_(None))
        ).one()