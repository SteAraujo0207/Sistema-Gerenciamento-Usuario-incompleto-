"""
Script para criar o primeiro usuário (gerente) do sistema.
Precisa existir pelo menos um gerente para conseguir cadastrar os demais,
já que o cadastro de usuários exige estar logado.

Como rodar (uma única vez):
    python seed.py
"""

from app.database import init_db, get_db
from app.security import hash_password


def seed():
    init_db()
    with get_db() as conn:
        existe = conn.execute(
            "SELECT id FROM usuarios WHERE cargo = 'gerente' LIMIT 1"
        ).fetchone()
        if existe:
            print("Já existe um gerente cadastrado. Nada foi alterado.")
            return

        conn.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, cargo) VALUES (?, ?, ?, ?)",
            (
                "Administrador Geral",
                "gerente@empresa.com",
                hash_password("Senha@123"),
                "gerente",
            ),
        )

    print("Gerente inicial criado com sucesso!")
    print("   E-mail: gerente@empresa.com")
    print("   Senha:  Senha@123")
    print("Troque essa senha assim que possível.")


if __name__ == "__main__":
    seed()
