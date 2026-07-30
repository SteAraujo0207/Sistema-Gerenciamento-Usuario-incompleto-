"""
Schemas Pydantic: definem o "formato" dos dados que entram e saem da API,
e fazem a validação automática (ex: e-mail válido, senha forte, etc).
"""

from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.security import validar_forca_senha

CargoType = Literal["gerente", "administrador", "usuario"]


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cargo: CargoType

    @field_validator("senha")
    @classmethod
    def senha_forte(cls, v: str) -> str:
        erros = validar_forca_senha(v)
        if erros:
            raise ValueError(" ".join(erros))
        return v


class UsuarioUpdate(BaseModel):
    """Todos os campos são opcionais: o front manda só o que o usuário alterou."""
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    cargo: Optional[CargoType] = None
    ativo: Optional[bool] = None

    @field_validator("senha")
    @classmethod
    def senha_forte(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        erros = validar_forca_senha(v)
        if erros:
            raise ValueError(" ".join(erros))
        return v


class UsuarioOut(BaseModel):
    """O que a API devolve para o front. Repare que 'senha' nunca aparece aqui."""
    id: int
    nome: str
    email: EmailStr
    cargo: CargoType
    ativo: bool
    criado_em: str


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ExclusaoRequest(BaseModel):
    confirmar: bool
