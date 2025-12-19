from fastapi import APIRouter

router = APIRouter(prefix="/motoristas", tags=["Motoristas"])

@router.get("/{cpf}/historico")
async def historico_motorista(cpf: str):
    return {"cpf": cpf, "abastecimentos": []}