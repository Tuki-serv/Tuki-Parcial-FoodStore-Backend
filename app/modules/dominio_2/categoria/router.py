from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from app.core.database import SessionDep
from app.modules.dominio_2.categoria.schemas import CategoriaRead, CategoriaCreate, CategoriaUpdate, CategoriaList, CategoriaWithChildren
from app.modules.dominio_2.categoria.service import CategoriaService
from app.modules.dominio_2.categoria.unit_of_work import CategoriaUnitOfWork

router = APIRouter(prefix="/categorias", tags=["Categorías"])

def get_categoria_service(session: SessionDep):
    uow = CategoriaUnitOfWork(session)
    return CategoriaService(uow)

CategoriaServiceDep = Annotated[CategoriaService, Depends(get_categoria_service)]

@router.get("/", response_model=CategoriaList)
def list_categorias(
    service: CategoriaServiceDep,
    offset: Annotated[int, Query(ge=0, description="Registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de registros")] = 20
):
    return service.get_all(offset=offset, limit=limit)

@router.get("/{id}", response_model=CategoriaWithChildren)
def get_categoria(id: int, service: CategoriaServiceDep):
    return service.get_by_id(id)

@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria_in: CategoriaCreate, service: CategoriaServiceDep):
    return service.create(categoria_in)

@router.put("/{id}", response_model=CategoriaRead)
def update_categoria(id: int, categoria_in: CategoriaUpdate, service: CategoriaServiceDep):
    return service.update(id, categoria_in)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_categoria(id: int, service: CategoriaServiceDep):
    return service.delete(id)