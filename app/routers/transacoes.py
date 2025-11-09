from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.database import get_db
from app.models.conta import Conta
from app.models.transacao import Transacao, TipoTransacao
from app.models.usuario import Usuario
from app.schemas.transacao import TransacaoCreate, TransacaoResponse, ExtratoResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/transacoes", tags=["Transações"])


@router.post("", response_model=TransacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_transacao(
    transacao_data: TransacaoCreate,
    conta_id: int = Query(..., description="ID da conta corrente"),
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova transação (depósito ou saque) em uma conta.
    
    - **conta_id**: ID da conta (query parameter)
    - **tipo**: Tipo de transação ('deposito' ou 'saque')
    - **valor**: Valor da transação (deve ser maior que zero)
    - **descricao**: Descrição opcional da transação
    
    Validações:
    - Não permite valores negativos ou zero
    - Para saques, verifica se há saldo suficiente
    
    Requer autenticação JWT. Só permite transações em contas do usuário autenticado.
    """
    # Verificar se a conta existe e pertence ao usuário
    result = await db.execute(
        select(Conta).where(Conta.id == conta_id, Conta.usuario_id == current_user.id)
    )
    conta = result.scalar_one_or_none()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    # Validação: valor deve ser positivo (já validado pelo Pydantic, mas garantindo)
    if transacao_data.valor <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor da transação deve ser maior que zero"
        )
    
    # Validação para saque: verificar saldo suficiente
    if transacao_data.tipo == TipoTransacao.SAQUE:
        if conta.saldo < transacao_data.valor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Saldo insuficiente. Saldo atual: R$ {conta.saldo:.2f}"
            )
        conta.saldo -= transacao_data.valor
    else:  # DEPOSITO
        conta.saldo += transacao_data.valor
    
    # Criar transação
    new_transacao = Transacao(
        tipo=transacao_data.tipo,
        valor=transacao_data.valor,
        descricao=transacao_data.descricao,
        conta_id=conta.id
    )
    
    db.add(new_transacao)
    await db.commit()
    await db.refresh(new_transacao)
    
    return new_transacao


@router.get("/extrato/{conta_id}", response_model=ExtratoResponse)
async def obter_extrato(
    conta_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtém o extrato completo de uma conta, incluindo todas as transações.
    
    - **conta_id**: ID da conta
    
    Retorna:
    - Informações da conta
    - Saldo atual
    - Lista de todas as transações (histórico completo)
    - Total de transações
    
    Requer autenticação JWT. Só retorna extratos de contas do usuário autenticado.
    """
    # Verificar se a conta existe e pertence ao usuário
    result = await db.execute(
        select(Conta).where(Conta.id == conta_id, Conta.usuario_id == current_user.id)
    )
    conta = result.scalar_one_or_none()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    # Buscar transações ordenadas por data (mais recentes primeiro)
    transacoes_result = await db.execute(
        select(Transacao)
        .where(Transacao.conta_id == conta_id)
        .order_by(desc(Transacao.created_at))
    )
    transacoes = transacoes_result.scalars().all()
    
    return ExtratoResponse(
        conta_id=conta.id,
        numero_conta=conta.numero,
        titular=conta.titular,
        saldo_atual=conta.saldo,
        transacoes=transacoes,
        total_transacoes=len(transacoes)
    )

