from typing import Generic, TypeVar, Type, Any
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlmodel import SQLModel
from datetime import datetime, timezone

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class base_service(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, uow: Any, repo_name: str, model_class: Type[ModelType]):
        """
        uow: La instancia de la unidad de trabajo (ej. CategoriaUnitOfWork)
        repo_name: El nombre del atributo del repositorio en la UoW (ej. 'categorias')
        model_class: La clase de la entidad para instanciarla en el create (ej. Categoria)
        """
        self.uow = uow
        self.repo_name = repo_name
        self.model_class = model_class

    @property
    def _repo(self):
        return getattr(self.uow, self.repo_name)
    
    def get_all(self, offset: int = 0, limit: int = 20):
        with self.uow as uow:
            items = self._repo.get_all_by_state(offset=offset, limit= limit)
            total = self._repo.count_model()
            return {"data": items, "total": total}
        
    def _get_or_404(self, item_id) -> ModelType:
        item = self._repo.get_by_id(item_id)
        if not item or getattr(item, "deleted_at", None) is not None:
            raise HTTPException(status_code=404, detail=f"{self.model_class.__name__} not found")
        return item

    def get_by_id(self, item_id: int | str) -> ModelType:
        with self.uow as uow:
            return self._get_or_404(item_id)
        
    def create(self, item_in: CreateSchemaType) -> ModelType:
        with self.uow as uow:
            nuevo_item = self.model_class(**item_in.model_dump())
            self._repo.add(nuevo_item)
            return nuevo_item
        
    def update(self, item_id: int | str, item_in: UpdateSchemaType) -> ModelType:
        item_db = self.get_by_id(item_id)
        with self.uow as uow:

            update_data = item_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(item_db, key, value)

            if hasattr(item_db, "updated_at"):
                item_db.updated_at = datetime.now(timezone.utc)

            self._repo.update(item_db)
            return item_db
        
    def delete(self, item_id: int | str):
        item_db = self.get_by_id(item_id)
        if hasattr(item_db, "deleted_at"):
            item_db.deleted_at = datetime.now(timezone.utc)
        
        self.update(item_id, item_db)

        return {"message": f"{self.model_class.__name__} elminado/a correctamente"}