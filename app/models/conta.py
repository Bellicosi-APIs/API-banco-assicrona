from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True, nullable=False)
    titular = Column(String, nullable=False)
    saldo = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relationships
    transacoes = relationship("Transacao", back_populates="conta", cascade="all, delete-orphan")
    usuario = relationship("Usuario", back_populates="contas")

