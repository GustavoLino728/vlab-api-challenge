from pathlib import Path
import sys
from decimal import Decimal
from app.models.abastecimento import TipoCombustivel
from app.repositories.abastecimento_repo import AbastecimentoRepository
from app.services.abastecimento_service import AbastecimentoService


class DummyRepo(AbastecimentoRepository):
    async def create(self, session, data, improper_data: bool):
        return {"improper_data": improper_data}


def make_service() -> AbastecimentoService:
    return AbastecimentoService(repo=DummyRepo())


def test_improper_false_when_price_below_or_equal_25_percent():
    service = make_service()
    media = service._media_mock(TipoCombustivel.GASOLINA)

    assert service._is_improper(media, media) is False

    limite = media * Decimal("1.25")
    assert service._is_improper(limite, media) is False


def test_improper_true_when_price_above_25_percent():
    service = make_service()
    media = service._media_mock(TipoCombustivel.GASOLINA)

    acima = media * Decimal("1.26")
    assert service._is_improper(acima, media) is True
