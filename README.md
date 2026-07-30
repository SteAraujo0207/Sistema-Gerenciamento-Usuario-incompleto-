# Sistema de Gerenciamento de Usuários — Back-end

API REST em **Python (FastAPI)** com banco de dados **SQL (SQLite)** para o
Sistema de Gerenciamento de Usuários. Responsável por: login/autenticação,
cadastro, consulta, alteração, exclusão e controle de permissões por hierarquia.

## Tecnologias

- **Python 3.11+**
- **FastAPI** — framework da API
- **SQLite** (via `sqlite3`, nativo do Python) — banco de dados
- **JWT** (`python-jose`) — token de autenticação
- **Passlib + bcrypt** — hash de senha
- **Pydantic** — validação de dados

## Estrutura do projeto

```
backend/
├── app/
│   ├── main.py          # ponto de entrada da API
│   ├── config.py        # variáveis de ambiente
│   ├── database.py       # conexão com o SQLite
│   ├── security.py       # hash de senha, validação de senha forte, JWT
│   ├── permissions.py    # regras de hierarquia (gerente/administrador/usuario)
│   ├── schemas.py        # validação dos dados de entrada/saída
│   ├── deps.py            # identifica o usuário logado a partir do token
│   └── routers/
│       ├── auth.py        # rota de login
│       └── usuarios.py    # CRUD de usuários
├── schema.sql             # criação das tabelas do banco
├── seed.py                # cria o primeiro usuário (gerente)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Como rodar no VS Code

1. Abra a pasta `backend` no VS Code.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Copie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
5. Crie o primeiro usuário (gerente):
   ```bash
   python seed.py
   ```
6. Rode a API:
   ```bash
   uvicorn app.main:app --reload
   ```
7. Acesse a documentação interativa (gerada automaticamente) em:
   ```
   http://127.0.0.1:8000/docs
   ```
   Nela dá pra testar todas as rotas direto pelo navegador, sem precisar do front-end ainda.

## Login inicial (criado pelo seed.py)

- **E-mail:** gerente@empresa.com
- **Senha:** Senha@123

Troque essa senha assim que possível (editando o próprio cadastro após o login).

## Principais rotas

| Método | Rota              | O que faz                                  |
|--------|-------------------|---------------------------------------------|
| POST   | `/auth/login`     | Autentica e devolve um token JWT             |
| POST   | `/usuarios`       | Cadastra um novo usuário                     |
| GET    | `/usuarios`       | Lista usuários (respeitando a hierarquia)    |
| GET    | `/usuarios/{id}`  | Consulta um usuário por ID                   |
| PUT    | `/usuarios/{id}`  | Altera dados cadastrais                      |
| DELETE | `/usuarios/{id}`  | Exclui um usuário (exige `confirmar: true`)  |

Todas as rotas de `/usuarios` exigem o token do login no cabeçalho:
```
Authorization: Bearer <token recebido no login>
```

## Regras de permissão (hierarquia)

| Cargo          | Pode ver                                  |
|----------------|--------------------------------------------|
| `gerente`      | Todos os cadastros                          |
| `administrador`| O próprio cadastro + usuários comuns        |
| `usuario`      | Apenas o próprio cadastro                   |

## Próximos passos

- Front-end em TypeScript consumindo esta API.
- Deploy do banco de dados (hoje é SQLite local, ideal para desenvolvimento/apresentação).
