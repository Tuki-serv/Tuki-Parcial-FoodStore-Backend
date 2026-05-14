from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.modules.dominio_2.categoria.models import Categoria
from app.modules.dominio_2.categoria.schemas import CategoriaCreate, CategoriaUpdate
from app.modules.dominio_2.categoria.unit_of_work import CategoriaUnitOfWork

class CategoriaService:
    def __init__(self, uow: CategoriaUnitOfWork):
        self.uow = uow

    def get_all(self, offset: int = 0, limit: int = 20):
        """
        Devuelve la estructura exacta que pide el Schema de paginación (data y total).
        """
        with self.uow as uow:
            categorias = uow.categorias.get_active(offset=offset, limit=limit)
            total = uow.categorias.count_active()
            return {"data": categorias, "total": total}

    def get_by_id(self, categoria_id: int):
        with self.uow as uow:
            categoria = uow.categorias.get_by_id(categoria_id)
            # Validamos que exista y que no esté borrada lógicamente
            if not categoria or categoria.deleted_at is not None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con id {categoria_id} no encontrada."
                )
        return categoria

    def create(self, categoria_in: CategoriaCreate):
        with self.uow as uow:
            # 1. Validar que no exista una categoría con el mismo nombre (Activa)
            existe = uow.categorias.get_by_nombre(categoria_in.nombre)
            if existe and existe.deleted_at is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una categoría activa con el nombre '{categoria_in.nombre}'."
                )
            
            # 2. Si nos mandan un parent_id, hay que validar que esa categoría "padre" exista
            if categoria_in.parent_id:
                parent = uow.categorias.get_by_id(categoria_in.parent_id)
                if not parent or parent.deleted_at is not None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"La categoría padre con id {categoria_in.parent_id} no existe."
                    )

            # 3. Mapear schema a modelo y guardar
            nueva_categoria = Categoria(**categoria_in.model_dump())
            uow.categorias.add(nueva_categoria)
            # El UnitOfWork hace el commit automáticamente al salir del bloque "with"
        return nueva_categoria

    def update(self, categoria_id: int, categoria_in: CategoriaUpdate):
        with self.uow as uow:
            # 1. Traer la original (reutilizamos el método get_by_id que ya lanza el 404)
            categoria_db = self.get_by_id(categoria_id)

            # 2. Si cambia el nombre, validar que el nuevo no choque con otro existente
            if categoria_in.nombre and categoria_in.nombre != categoria_db.nombre:
                existe = uow.categorias.get_by_nombre(categoria_in.nombre)
                if existe and existe.deleted_at is None:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="El nombre ya está en uso por otra categoría."
                    )

            # 3. Si cambia el padre, validar que exista y que no se asigne a sí misma
            if categoria_in.parent_id is not None and categoria_in.parent_id != categoria_db.parent_id:
                if categoria_in.parent_id == categoria_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Una categoría no puede ser padre de sí misma."
                    )
                parent = uow.categorias.get_by_id(categoria_in.parent_id)
                if not parent or parent.deleted_at is not None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="La nueva categoría padre no existe."
                    )

            # 4. Aplicar cambios solo de los campos que se enviaron
            update_data = categoria_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(categoria_db, key, value)
            
            categoria_db.updated_at = datetime.now(timezone.utc)
            uow.categorias.update(categoria_db)
        return categoria_db

    def delete(self, categoria_id: int):
        with self.uow as uow:
            categoria_db = self.get_by_id(categoria_id)
            
            # Aplicamos el BORRADO LÓGICO
            categoria_db.deleted_at = datetime.now(timezone.utc)
            uow.categorias.update(categoria_db)
            
        return {"mensaje": f"Categoría {categoria_id} eliminada correctamente"}