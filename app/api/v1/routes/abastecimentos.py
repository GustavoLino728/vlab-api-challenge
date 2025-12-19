from fastapi import APIRouter
from app.schemas.abastecimento import AbastecimentoCreate

router = APIRouter(prefix="/abastecimentos", tags=["Abastecimentos"])

@router.post("")
async def criar_abastecimento(payload: AbastecimentoCreate):
    return payload

@router.get("")
async def listar_abastecimentos():
    return {"items": [], "page": 1, "size": 10}