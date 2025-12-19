from sqlalchemu.ext.asyncio import AsyncSession
from app.models.abastecimento import Abastecimento
from app.schemas.abastecimento import AbastecimentoCreate


class AbastecimentoRepository:
    async def create(self, session: AsyncSession, data: AbastecimentoCreate, improper_data: bool) -> Abastecimento:
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