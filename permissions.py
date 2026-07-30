"""
Regras de permissão de acordo com a hierarquia de cargos.

Hierarquia (do maior para o menor nível):
    gerente        -> vê e gerencia todo mundo
    administrador  -> vê a si mesmo e os usuários comuns
    usuario        -> vê apenas a si mesmo
"""

HIERARQUIA = {"gerente": 3, "administrador": 2, "usuario": 1}


def nivel(cargo: str) -> int:
    return HIERARQUIA.get(cargo, 0)


def pode_visualizar(usuario_logado: dict, usuario_alvo: dict) -> bool:
    """Todo mundo pode ver o próprio cadastro; acima disso, depende da hierarquia."""
    if usuario_logado["id"] == usuario_alvo["id"]:
        return True
    if usuario_logado["cargo"] == "gerente":
        return True
    return nivel(usuario_logado["cargo"]) > nivel(usuario_alvo["cargo"])


def pode_editar(usuario_logado: dict, usuario_alvo: dict) -> bool:
    return pode_visualizar(usuario_logado, usuario_alvo)


def pode_excluir(usuario_logado: dict, usuario_alvo: dict) -> bool:
    """Ninguém pode excluir o próprio usuário por aqui (evita se auto-excluir sem querer)."""
    if usuario_logado["id"] == usuario_alvo["id"]:
        return False
    if usuario_logado["cargo"] == "gerente":
        return True
    return nivel(usuario_logado["cargo"]) > nivel(usuario_alvo["cargo"])


def pode_cadastrar(usuario_logado: dict, cargo_novo: str) -> bool:
    """Usuário comum não pode cadastrar ninguém. Gerente pode cadastrar qualquer cargo."""
    if usuario_logado["cargo"] == "usuario":
        return False
    if usuario_logado["cargo"] == "gerente":
        return True
    return nivel(usuario_logado["cargo"]) > nivel(cargo_novo)
