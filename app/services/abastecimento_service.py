from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.abastecimento import Abastecimento, TipoCombustivel
from app.repositories.abastecimento_repo import AbastecimentoRepository
from app.schemas.abastecimento import AbastecimentoCreate

class AbastecimentoService:
    def __init__(self, repo: AbastecimentoRepository) -> None:
        self.repo = repo
        
    def _media_mock(self, tipo: TipoCombustivel) -> Decimal:
        if tipo == TipoCombustivel.GASOLINA:
            return Decimal("5.50")
        if tipo == TipoCombustivel.ETANOL:
            return Decimal("3.80")
        else:
            return Decimal("6.20")
        
    def _is_improper(self, preco: Decimal, media: Decimal) -> bool:
        if preco > media + (media*0.75):
            return True
        else:
            return False
        
    async def criar(self, session: AsyncSession, data: AbastecimentoCreate) -> Abastecimento:
        media = self._media_mock(data.tipo_combustivel)
        improper = self._is_improper(data.preco_por_litro, media)
        return await self.repo.create(session=session, data=data, improper_data=improper)