from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ContaBase(BaseModel):
    numero: str = Field(..., description="Número da conta corrente", example="12345-6")
    titular: str = Field(..., description="Nome do titular da conta", example="João Silva")


class ContaCreate(ContaBase):
    pass


class ContaResponse(ContaBase):
    id: int
    saldo: float = Field(..., description="Saldo atual da conta", example=1000.50)
    created_at: datetime
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)


class ContaList(BaseModel):
    id: int
    numero: str
    titular: str
    saldo: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

