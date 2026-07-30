"""
Funções de segurança:
- hash e verificação de senha (nunca guardamos senha em texto puro)
- validação de força da senha
- criação e leitura de tokens JWT (usados no login)
"""

import re
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(senha: str) -> str:
    return pwd_context.hash(senha)


def verify_password(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def validar_forca_senha(senha: str) -> list[str]:
    """
    Regras de senha forte. Retorna uma lista de erros (vazia = senha válida).
    Ajuste as regras aqui se o seu projeto pedir outras exigências.
    """
    erros = []
    if len(senha) < 8:
        erros.append("A senha deve ter no mínimo 8 caracteres.")
    if not re.search(r"[A-Z]", senha):
        erros.append("A senha deve ter ao menos uma letra maiúscula.")
    if not re.search(r"[a-z]", senha):
        erros.append("A senha deve ter ao menos uma letra minúscula.")
    if not re.search(r"[0-9]", senha):
        erros.append("A senha deve ter ao menos um número.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", senha):
        erros.append("A senha deve ter ao menos um caractere especial (ex: ! @ # $ %).")
    return erros


def criar_token(dados: dict) -> str:
    to_encode = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
