from datetime import date
from typing import Iterable

from sqlalchemy import Select, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.abastecimento import Abastecimento
from app.schemas.abastecimento import AbastecimentoCreate


class AbastecimentoRepository:
    async def create(
        self, session: AsyncSession, data: AbastecimentoCreate, improper_data: bool
    ) -> Abastecimento:
        obj = Abastecimento(
            id_posto=data.id_posto,
            data_hora=data.data_hora,
            tipo_combustivel=data.tipo_combustivel,
            preco_por_litro=data.preco_por_litro,
            volume_abastecido=data.volume_abastecido,
            cpf_motorista=data.cpf_motorista,
            improper_data=improper_data,
        )

        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def list_paginated(
        self,
        session: AsyncSession,
        *,
        page: int,
        size: int,
        tipo_combustivel: str | None = None,
        data: date | None = None,
    ) -> tuple[int, list[Abastecimento]]:
        query: Select[tuple[Abastecimento]] = select(Abastecimento)

        if tipo_combustivel:
            query = query.where(Abastecimento.tipo_combustivel == tipo_combustivel)

        if data:
            query = query.where(func.date(Abastecimento.data_hora) == data)

        count_query = select(func.count()).select_from(query.subquery())
        total = (await session.execute(count_query)).scalar_one()

        offset = (page - 1) * size
        query = query.order_by(desc(Abastecimento.data_hora)).offset(offset).limit(size)

        result = await session.execute(query)
        items: Iterable[Abastecimento] = result.scalars().all()
        return total, list(items)

    async def list_by_cpf(self, session: AsyncSession, cpf: str) -> list[Abastecimento]:
        query = (
            select(Abastecimento)
            .where(Abastecimento.cpf_motorista == cpf)
            .order_by(desc(Abastecimento.data_hora))
        )

        result = await session.execute(query)
        return list(result.scalars().all())
