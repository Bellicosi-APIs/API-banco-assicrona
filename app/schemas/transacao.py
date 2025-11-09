from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List
from app.models.transacao import TipoTransacao


class TransacaoBase(BaseModel):
    valor: float = Field(..., gt=0, description="Valor da transação (deve ser maior que zero)", example=100.00)
    descricao: Optional[str] = Field(None, description="Descrição opcional da transação", example="Depósito inicial")

    @field_validator("valor")
    @classmethod
    def validate_valor(cls, v):
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return v


class TransacaoCreate(TransacaoBase):
    tipo: TipoTransacao = Field(..., description="Tipo de transação: 'deposito' ou 'saque'", example=TipoTransacao.DEPOSITO)


class TransacaoResponse(TransacaoBase):
    id: int
    tipo: TipoTransacao
    created_at: datetime
    conta_id: int

    model_config = ConfigDict(from_attributes=True)


class ExtratoResponse(BaseModel):
    conta_id: int
    numero_conta: str
    titular: str
    saldo_atual: float
    transacoes: List[TransacaoResponse]
    total_transacoes: int

    model_config = ConfigDict(from_attributes=True)

