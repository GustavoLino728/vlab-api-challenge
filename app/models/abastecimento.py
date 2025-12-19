import enum
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class TipoCombustivel(str, enum.Enum):
    GASOLINA = "GASOLINA"
    ETANOL = "ETANOL"
    DIESEL = "DIESEL"


class Abastecimento(Base):
    __tablename__ = "abastecimentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_posto: Mapped[int] = mapped_column(Integer, nullable=False)
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tipo_combustivel: Mapped[TipoCombustivel] = mapped_column(Enum(TipoCombustivel), nullable=False)
    preco_por_litro: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    volume_abastecido: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    cpf_motorista: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    improper_data: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)