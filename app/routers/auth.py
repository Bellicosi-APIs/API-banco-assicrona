from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token
from app.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """
    Cria um novo usuário no sistema.
    
    - **username**: Nome de usuário único (mínimo 3 caracteres)
    - **email**: Email único do usuário
    - **password**: Senha (mínimo 6 caracteres)
    """
    try:
        # Verificar se username já existe
        result = await db.execute(select(Usuario).where(Usuario.username == user_data.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso"
            )
        
        # Verificar se email já existe
        result = await db.execute(select(Usuario).where(Usuario.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
        
        # Criar novo usuário
        hashed_password = get_password_hash(user_data.password)
        new_user = Usuario(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        # Log do erro para debug
        import traceback
        print(f"Erro ao criar usuário: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(user_credentials: UsuarioLogin, db: AsyncSession = Depends(get_db)):
    """
    Autentica um usuário e retorna um token JWT.
    
    - **username**: Nome de usuário
    - **password**: Senha do usuário
    
    Retorna um token de acesso que deve ser usado nos headers das requisições protegidas:
    `Authorization: Bearer <token>`
    """
    user = await authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioResponse)
async def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """
    Retorna informações do usuário atual autenticado.
    
    Requer autenticação JWT.
    """
    return current_user

