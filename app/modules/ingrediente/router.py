from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from app.core.database import SessionDep
from app.modules.ingrediente.schemas import IngredienteRead, IngredienteCreate, IngredienteUpdate, IngredienteList, IngredienteFullRead
from app.modules.ingrediente.service import IngredienteService
from app.modules.ingrediente.unit_of_work import IngredienteUnitOfWork

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

def get_ingrediente_service(session: SessionDep):
    uow = IngredienteUnitOfWork(session)
    return IngredienteService(uow)

IngredienteServiceDep = Annotated[IngredienteService, Depends(get_ingrediente_service)]

@router.get("/", response_model=IngredienteList)
def list_ingredientes(
    service: IngredienteServiceDep,
    offset: Annotated[int, Query(ge=0, description="Registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de registros")] = 20
):
    return service.get_all(offset=offset, limit=limit)

@router.get("/{id}", response_model=IngredienteFullRead)
def get_ingrediente(id: int, service: IngredienteServiceDep):
    return service.get_by_id(id)

@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def create_ingrediente(ingrediente_in: IngredienteCreate, service: IngredienteServiceDep):
    return service.create(ingrediente_in)

@router.put("/{id}", response_model=IngredienteRead)
def update_ingrediente(id: int, ingrediente_in: IngredienteUpdate, service: IngredienteServiceDep):
    return service.update(id, ingrediente_in)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_ingrediente(id: int, service: IngredienteServiceDep):
    return service.delete(id)