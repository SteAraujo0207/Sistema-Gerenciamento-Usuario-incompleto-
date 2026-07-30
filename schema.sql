-- Tabela principal de usuários do sistema
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- ID gerado automaticamente
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,                  -- nunca guardamos a senha em texto puro
    cargo TEXT NOT NULL CHECK (cargo IN ('gerente', 'administrador', 'usuario')),
    ativo INTEGER NOT NULL DEFAULT 1,          -- 1 = ativo, 0 = inativo (soft delete futuro, se quiser)
    criado_em TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Índice para acelerar buscas por e-mail (usado no login)
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
