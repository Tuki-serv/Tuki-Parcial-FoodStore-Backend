from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, Query, status
from app.core.database import SessionDep
from app.modules.dominio_2.producto.schemas import ProductoRead, ProductoCreate, ProductoUpdate, ProductoList, ProductoFullRead
from app.modules.dominio_2.producto.service import ProductoService
from app.modules.dominio_2.producto.unit_of_work import ProductoUnitOfWork

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_producto_service(session: SessionDep):
    uow = ProductoUnitOfWork(session)
    return ProductoService(uow)

ProductoServiceDep = Annotated[ProductoService, Depends(get_producto_service)]

@router.get("/", response_model=ProductoList)
def list_productos(
    service: ProductoServiceDep,
    offset: Annotated[int, Query(ge=0, description="Registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de registros")] = 20,
    categoria_id: Annotated[Optional[List[int]], Query(description="Filtrar por IDs de Categoría")] = None,
    ingrediente_id: Annotated[Optional[List[int]], Query(description="Filtrar por IDs de Ingrediente")] = None
):
    return service.get_all(
        offset=offset, 
        limit=limit, 
        categoria_id=categoria_id, 
        ingrediente_id=ingrediente_id
    )

@router.get("/{id}", response_model=ProductoFullRead)
def get_producto(id: int, service: ProductoServiceDep):
    return service.get_by_id(id)

@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(producto_in: ProductoCreate, service: ProductoServiceDep):
    return service.create(producto_in)

@router.put("/{id}", response_model=ProductoRead)
def update_producto(id: int, producto_in: ProductoUpdate, service: ProductoServiceDep):
    return service.update(id, producto_in)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_producto(id: int, service: ProductoServiceDep):
    return service.delete(id)