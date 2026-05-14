from datetime import datetime, timezone
from fastapi import HTTPException
from app.modules.dominio_2.producto.models import Producto
from app.modules.dominio_2.producto_categoria.models import ProductoCategoria
from app.modules.dominio_2.producto_ingrediente.models import ProductoIngrediente
from app.modules.dominio_2.producto.schemas import ProductoCreate, ProductoUpdate
from app.modules.dominio_2.producto.unit_of_work import ProductoUnitOfWork
from typing import Optional, List

class ProductoService:
    def __init__(self, uow: ProductoUnitOfWork):
        self.uow = uow

    def get_all(self, offset: int = 0, limit: int = 20,categoria_id: Optional[List[int]] = None,ingrediente_id: Optional[List[int]] = None):
        with self.uow as uow:
            productos = uow.productos.get_active(offset=offset, limit=limit, categoria_id=categoria_id, ingrediente_id=ingrediente_id)
            total = uow.productos.count_active(
                categoria_id=categoria_id, 
                ingrediente_id=ingrediente_id
            )
        return {"data": productos, "total": total}
        
    def get_by_id(self, producto_id: int):
        with self.uow as uow:
            producto = uow.productos.get_by_id(producto_id)
            if not producto or producto.deleted_at is not None:
                raise HTTPException(
                    status_code=404, detail="Producto no encontrado"
                )

        return producto

    def create(self, producto_in: ProductoCreate):
        with self.uow as uow:
            # 1. Validar nombre duplicado
            if uow.productos.get_by_nombre(producto_in.nombre):
                raise HTTPException(status_code=409, detail="El producto ya existe")

            # 2. Crear instancia base (sin las listas de IDs)
            producto_data = producto_in.model_dump(exclude={"categoria_ids", "ingrediente_ids"})
            nuevo_producto = Producto(**producto_data)
            uow.productos.add(nuevo_producto) 

            # 3. Relaciones Complejas: Categorías
            for idx, cat_id in enumerate(producto_in.categoria_ids):
                categoria = uow.categorias.get_by_id(cat_id)
                if not categoria:
                    raise HTTPException(status_code=400, detail=f"Categoría {cat_id} no existe")
                
                # Definimos la primer categoria como principal por defecto
                es_principal = True if idx == 0 else False
                link_cat = ProductoCategoria(producto_id=nuevo_producto.id, categoria_id=cat_id, es_principal=es_principal)
                uow._session.add(link_cat)

            # 4. Relaciones Complejas: Ingredientes
            for ing_id in producto_in.ingrediente_ids:
                ingrediente = uow.ingredientes.get_by_id(ing_id)
                if not ingrediente:
                    raise HTTPException(status_code=400, detail=f"Ingrediente {ing_id} no existe")
                
                link_ing = ProductoIngrediente(producto_id=nuevo_producto.id, ingrediente_id=ing_id)
                uow._session.add(link_ing)

        return nuevo_producto
        
    def update(self, producto_id: int, producto_in: ProductoUpdate):
        with self.uow as uow:
            producto_db = uow.productos.get_by_id(producto_id)
            if not producto_db or producto_db.deleted_at is not None:
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            update_data = producto_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(producto_db, key, value)
            
            producto_db.updated_at = datetime.now(timezone.utc)
            uow.productos.update(producto_db)
        return producto_db

    def delete(self, producto_id: int):
        with self.uow as uow:
            producto = uow.productos.get_by_id(producto_id)
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            
            producto.deleted_at = datetime.now(timezone.utc)
            uow.productos.update(producto)
        return {"mensaje": "Producto eliminado (lógico)"}