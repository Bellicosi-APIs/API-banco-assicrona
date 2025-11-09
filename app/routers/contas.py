from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.conta import Conta
from app.models.usuario import Usuario
from app.schemas.conta import ContaCreate, ContaResponse, ContaList
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/contas", tags=["Contas"])


@router.post("", response_model=ContaResponse, status_code=status.HTTP_201_CREATED)
async def criar_conta(
    conta_data: ContaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova conta corrente.
    
    - **numero**: Número da conta corrente (único)
    - **titular**: Nome do titular da conta
    
    Requer autenticação JWT.
    """
    # Verificar se número de conta já existe
    result = await db.execute(select(Conta).where(Conta.numero == conta_data.numero))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de conta já está em uso"
        )
    
    # Criar nova conta
    new_conta = Conta(
        numero=conta_data.numero,
        titular=conta_data.titular,
        saldo=0.0,
        usuario_id=current_user.id
    )
    
    db.add(new_conta)
    await db.commit()
    await db.refresh(new_conta)
    
    return new_conta


@router.get("", response_model=List[ContaList])
async def listar_contas(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Lista todas as contas do usuário autenticado.
    
    Requer autenticação JWT.
    """
    result = await db.execute(
        select(Conta).where(Conta.usuario_id == current_user.id)
    )
    contas = result.scalars().all()
    return contas


@router.get("/{conta_id}", response_model=ContaResponse)
async def obter_conta(
    conta_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtém detalhes de uma conta específica.
    
    - **conta_id**: ID da conta
    
    Requer autenticação JWT. Só retorna contas do usuário autenticado.
    """
    result = await db.execute(
        select(Conta).where(Conta.id == conta_id, Conta.usuario_id == current_user.id)
    )
    conta = result.scalar_one_or_none()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    return conta

