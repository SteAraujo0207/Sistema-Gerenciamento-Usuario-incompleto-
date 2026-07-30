"""
Dependência usada em todas as rotas protegidas.
Lê o token JWT enviado no cabeçalho "Authorization: Bearer <token>",
valida e devolve os dados do usuário logado (para usar nas checagens de permissão).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_usuario_logado(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado. Faça login novamente.",
        )

    with get_db() as conn:
        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE id = ? AND ativo = 1", (payload.get("sub"),)
        ).fetchone()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo.",
        )

    return dict(usuario)
