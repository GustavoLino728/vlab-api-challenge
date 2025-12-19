from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from app.utils.cpf import is_valid_cpf, only_digits

class TipoCombustivel(str, Enum):
    GASOLINA = "GASOLINA"
    ETANOL = "ETANOL"
    DIESEL = "DIESEL"
    
class AbastecimentoCreate(BaseModel):
    id_posto: int = Field(..., ge=1)
    data_hora: datetime
    tipo_combustivel: TipoCombustivel
    preco_por_litro: Decimal = Field(..., gt=0)
    volume_abastecido: Decimal = Field(..., gt=0)
    cpf_motorista: str
    
    @field_validator("cpf_motorista")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        digits = only_digits(v)
        if not is_valid_cpf(digits):
            raise ValueError("CPF Inválido")
        return digits
    
class AbastecimentoOut(BaseModel):
    id: int
    id_posto: int
    data_hora: datetime
    tipo_combustivel: TipoCombustivel
    preco_por_litro: Decimal
    volume_abastecido: Decimal
    cpf_motorista: str
    improper_data: bool
    
    class Config:
        from_attributes = True