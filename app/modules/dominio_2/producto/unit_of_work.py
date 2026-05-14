from sqlmodel import Session
from app.core.unit_of_work import UnitOfWork
from app.modules.dominio_2.producto.repository import ProductoRepository
from app.modules.dominio_2.categoria.repository import CategoriaRepository
from app.modules.dominio_2.ingrediente.repository import IngredienteRepository

class ProductoUnitOfWork(UnitOfWork):
    def __init__(self, session: Session):
        super().__init__(session)
        self.productos = ProductoRepository(session)
        self.categorias = CategoriaRepository(session)
        self.ingredientes = IngredienteRepository(session)