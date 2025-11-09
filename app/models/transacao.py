from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class TipoTransacao(str, enum.Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoTransacao), nullable=False)
    valor = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)

    # Relationships
    conta = relationship("Conta", back_populates="transacoes")

