from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, description="Nome de usuário", example="joao_silva")
    email: EmailStr = Field(..., description="Email do usuário", example="joao@example.com")


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, description="Senha do usuário (mínimo 6 caracteres)", example="senha123")


class UsuarioResponse(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UsuarioLogin(BaseModel):
    username: str = Field(..., description="Nome de usuário", example="joao_silva")
    password: str = Field(..., description="Senha do usuário", example="senha123")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

