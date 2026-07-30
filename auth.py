"""
Rota de autenticação: recebe e-mail e senha, confere no banco de dados
e devolve um token JWT que o front-end vai usar nas próximas requisições.
"""

from fastapi import APIRouter, HTTPException, status

from app.database import get_db
from app.security import verify_password, criar_token
from app.schemas import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=Token)
def login(dados: LoginRequest):
    with get_db() as conn:
        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE email = ? AND ativo = 1", (dados.email,)
        ).fetchone()

    # Mensagem genérica de propósito: não revela se o erro foi no e-mail ou na senha
    if not usuario or not verify_password(dados.senha, usuario["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    token = criar_token({"sub": str(usuario["id"]), "cargo": usuario["cargo"]})
    return Token(access_token=token)
