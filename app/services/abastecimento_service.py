from decimal import Decimal
from datetime import date
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
        return preco > (media * Decimal("1.25"))

    async def create(
        self, session: AsyncSession, data: AbastecimentoCreate
    ) -> Abastecimento:
        media = self._media_mock(data.tipo_combustivel)
        improper = self._is_improper(data.preco_por_litro, media)
        return await self.repo.create(
            session=session, data=data, improper_data=improper
        )

    async def listar(
        self,
        session: AsyncSession,
        *,
        page: int,
        size: int,
        tipo_combustivel: str | None,
        data: date | None,
    ) -> tuple[int, list[Abastecimento]]:
        return await self.repo.list_paginated(
            session,
            page=page,
            size=size,
            tipo_combustivel=tipo_combustivel,
            data=data,
        )

    async def historico_motorista(
        self, session: AsyncSession, cpf: str
    ) -> list[Abastecimento]:
        return await self.repo.list_by_cpf(session, cpf)
