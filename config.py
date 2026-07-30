"""
Configurações centrais da aplicação.
Tudo que é "ajustável" (chave secreta, tempo de expiração do token,
caminho do banco de dados) fica aqui, lido a partir do arquivo .env.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # carrega as variáveis do arquivo .env, se existir

SECRET_KEY = os.getenv("SECRET_KEY", "troque-esta-chave-em-producao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
DATABASE_PATH = os.getenv("DATABASE_PATH", "sistema.db")
