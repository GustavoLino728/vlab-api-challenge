from datetime import date
from fastapi import APIRouter, Depends, Query, status
from app.api.deps import DbSession
from app.api.security import verify_api_key
from app.repositories.abastecimento_repo import AbastecimentoRepository
from app.schemas.abastecimento import AbastecimentoCreate, AbastecimentoOut
from app.schemas.pagination import Page
from app.services.abastecimento_service import AbastecimentoService
from app.utils.cpf import only_digits


router = APIRouter(prefix="/abastecimentos", tags=["Abastecimentos"])

service = AbastecimentoService(repo=AbastecimentoRepository())


@router.post(
    "",
    response_model=AbastecimentoOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
async def criar_abastecimento(payload: AbastecimentoCreate, db: DbSession):
    obj = await service.create(session=db, data=payload)
    return obj


@router.get("", response_model=Page[AbastecimentoOut])
async def listar_abastecimentos(
    db: DbSession,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    tipo_combustivel: str | None = Query(None),
    data: date | None = Query(None),
):
    total, items = await service.listar(
        session=db,
        page=page,
        size=size,
        tipo_combustivel=tipo_combustivel,
        data=data,
    )
    return Page[AbastecimentoOut](
        total=total,
        page=page,
        size=size,
        items=items,
    )
