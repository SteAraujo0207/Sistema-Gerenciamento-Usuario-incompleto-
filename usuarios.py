"""
Rotas do módulo de usuários:
- POST   /usuarios          -> cadastrar
- GET    /usuarios          -> listar (respeitando a hierarquia)
- GET    /usuarios/{id}     -> consultar por ID
- PUT    /usuarios/{id}     -> alterar dados
- DELETE /usuarios/{id}     -> excluir (exige confirmação)
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.deps import get_usuario_logado
from app.security import hash_password
from app.schemas import UsuarioCreate, UsuarioUpdate, UsuarioOut, ExclusaoRequest
from app import permissions

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


def _sem_senha(usuario) -> dict:
    """Remove o hash da senha antes de devolver o usuário para o front-end."""
    dados = dict(usuario)
    dados.pop("senha_hash", None)
    dados["ativo"] = bool(dados["ativo"])
    return dados


@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    dados: UsuarioCreate, usuario_logado: dict = Depends(get_usuario_logado)
):
    if not permissions.pode_cadastrar(usuario_logado, dados.cargo):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Você não tem permissão para cadastrar esse tipo de usuário.",
        )

    with get_db() as conn:
        existe = conn.execute(
            "SELECT id FROM usuarios WHERE email = ?", (dados.email,)
        ).fetchone()
        if existe:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Já existe um usuário com este e-mail."
            )

        cursor = conn.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, cargo) VALUES (?, ?, ?, ?)",
            (dados.nome, dados.email, hash_password(dados.senha), dados.cargo),
        )
        novo_id = cursor.lastrowid  # <- é aqui que pegamos o ID gerado automaticamente
        novo = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?", (novo_id,)
        ).fetchone()

    return _sem_senha(novo)


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios(usuario_logado: dict = Depends(get_usuario_logado)):
    with get_db() as conn:
        todos = conn.execute("SELECT * FROM usuarios").fetchall()

    visiveis = [
        _sem_senha(u) for u in todos if permissions.pode_visualizar(usuario_logado, dict(u))
    ]
    return visiveis


@router.get("/{usuario_id}", response_model=UsuarioOut)
def consultar_usuario(
    usuario_id: int, usuario_logado: dict = Depends(get_usuario_logado)
):
    with get_db() as conn:
        alvo = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()

    if not alvo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado.")
    if not permissions.pode_visualizar(usuario_logado, dict(alvo)):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Você não tem permissão para ver este usuário."
        )

    return _sem_senha(alvo)


@router.put("/{usuario_id}", response_model=UsuarioOut)
def alterar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    usuario_logado: dict = Depends(get_usuario_logado),
):
    with get_db() as conn:
        alvo = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
        if not alvo:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado.")
        if not permissions.pode_editar(usuario_logado, dict(alvo)):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Você não tem permissão para editar este usuário.",
            )

        campos = dados.model_dump(exclude_unset=True)  # só os campos que vieram no corpo
        if "senha" in campos:
            campos["senha_hash"] = hash_password(campos.pop("senha"))
        if not campos:
            return _sem_senha(alvo)

        set_clause = ", ".join(f"{campo} = ?" for campo in campos)
        valores = list(campos.values()) + [usuario_id]
        conn.execute(f"UPDATE usuarios SET {set_clause} WHERE id = ?", valores)

        atualizado = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()

    return _sem_senha(atualizado)


@router.delete("/{usuario_id}")
def excluir_usuario(
    usuario_id: int,
    confirmacao: ExclusaoRequest,
    usuario_logado: dict = Depends(get_usuario_logado),
):
    if not confirmacao.confirmar:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "É necessário confirmar a exclusão (envie confirmar: true).",
        )

    with get_db() as conn:
        alvo = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
        if not alvo:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado.")
        if not permissions.pode_excluir(usuario_logado, dict(alvo)):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Você não tem permissão para excluir este usuário.",
            )

        conn.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))

    return {"mensagem": f"Usuário {usuario_id} excluído com sucesso."}
