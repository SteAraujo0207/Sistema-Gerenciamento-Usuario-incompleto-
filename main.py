"""
Ponto de entrada da aplicação.
Roda com: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import auth, usuarios

app = FastAPI(
    title="Sistema de Gerenciamento de Usuários",
    description="API back-end (login, cadastro, consulta, alteração e exclusão de usuários com hierarquia de permissões).",
    version="1.0.0",
)

# Libera o acesso para o front-end (em produção, troque "*" pelo domínio do front)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)


@app.on_event("startup")
def ao_iniciar():
    init_db()


@app.get("/", tags=["Status"])
def status_api():
    return {"status": "online", "documentacao": "/docs"}
