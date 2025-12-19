from fastapi import APIRouter

router = APIRouter(prefix="/abastecimentos", tags=["Abastecimentos"])

@router.post("")
async def criar_abastecimento():
    return {"message": "TODO"}

@router.get("")
async def listar_abastecimentos():
    return {"items": [], "page": 1, "size": 10}