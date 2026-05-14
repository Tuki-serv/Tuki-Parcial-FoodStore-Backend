from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.modules.dominio_2.ingrediente.models import Ingrediente
from app.modules.dominio_2.ingrediente.schemas import IngredienteCreate, IngredienteUpdate
from app.modules.dominio_2.ingrediente.unit_of_work import IngredienteUnitOfWork

class IngredienteService:
    def __init__(self, uow: IngredienteUnitOfWork):
        self.uow = uow

    def get_all(self, offset: int = 0, limit: int = 20):
        with self.uow as uow:
            ingredientes = uow.ingredientes.get_active(offset=offset, limit=limit)
            total = uow.ingredientes.count_active()
        return {"data": ingredientes, "total": total}

    def get_by_id(self, ingrediente_id: int):
        with self.uow as uow:
            ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
            if not ingrediente or ingrediente.deleted_at is not None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Ingrediente no encontrado"
                )
        return ingrediente

    def create(self, ingrediente_in: IngredienteCreate):
        with self.uow as uow:
            if uow.ingredientes.get_by_nombre(ingrediente_in.nombre):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, 
                    detail="El ingrediente ya existe"
                )
            
            nuevo_ingrediente = Ingrediente(**ingrediente_in.model_dump())
            uow.ingredientes.add(nuevo_ingrediente)
        return nuevo_ingrediente

    def update(self, ingrediente_id: int, ingrediente_in: IngredienteUpdate):
        with self.uow as uow:
            ingrediente_db = self.get_by_id(ingrediente_id)
            
            update_data = ingrediente_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(ingrediente_db, key, value)
            
            ingrediente_db.updated_at = datetime.now(timezone.utc)
            uow.ingredientes.update(ingrediente_db)
        return ingrediente_db

    def delete(self, ingrediente_id: int):
        with self.uow as uow:
            ingrediente_db = self.get_by_id(ingrediente_id)
            
            # 
            ingrediente_db.deleted_at = datetime.now(timezone.utc)
            uow.ingredientes.update(ingrediente_db)
        return {"mensaje": f"Ingrediente {ingrediente_id} eliminado correctamente"}