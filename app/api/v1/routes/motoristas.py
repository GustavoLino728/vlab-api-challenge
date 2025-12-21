from fastapi import APIRouter, HTTPException
from app.api.deps import DbSession
from app.repositories.abastecimento_repo import AbastecimentoRepository
from app.schemas.abastecimento import AbastecimentoOut
from app.services.abastecimento_service import AbastecimentoService
from app.utils.cpf import is_valid_cpf, only_digits


router = APIRouter(prefix="/motoristas", tags=["Motoristas"])

service = AbastecimentoService(repo=AbastecimentoRepository())

@router.get("/{cpf}/historico", response_model=list[AbastecimentoOut])
async def historico_motorista(cpf: str, db: DbSession):
    digits = only_digits(cpf)
    if not is_valid_cpf(digits):
        raise HTTPException(status_code=400, detail="CPF inválido")

    items = await service.historico_motorista(session=db, cpf=digits)
    return items
