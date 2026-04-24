# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FlowCapital Credit Score — sistema de análise de crédito com autenticação baseada em CPF. Monorepo com backend Django e frontend Quasar/Vue 3, orquestrados via Docker Compose.

## Running the Project

### Docker (recommended — sobe tudo junto)
```bash
docker compose up --build
```
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:9000`

### Backend (local)
```bash
cd backend
uv run python manage.py migrate
uv run python manage.py runserver
```

### Frontend (local)
```bash
cd frontend
pnpm install
pnpm run dev
```

## Backend Commands

```bash
# Criar migrações após alterar models
uv run python manage.py makemigrations

# Aplicar migrações
uv run python manage.py migrate

# Criar superusuário (usa CPF como username)
uv run python manage.py createsuperuser
```

**Gerenciador de pacotes:** `uv` (não usar pip diretamente).  
**Python:** 3.12 (definido em `.python-version`).

## Frontend Commands

```bash
cd frontend

pnpm run dev       # dev server em localhost:9000
pnpm run build     # build de produção
pnpm run lint      # ESLint
pnpm run format    # Prettier
```

**Gerenciador de pacotes:** `pnpm` (lockfile version 9). Não usar npm ou yarn para instalar pacotes.

## Architecture

### Backend (`backend/`)

Django 6 + Django REST Framework + Token Authentication.

- **`core/`** — configuração do projeto (settings, urls raiz, wsgi/asgi)
- **`autenticacao/`** — app de autenticação

**Modelo de usuário:** `autenticacao.Usuario` substitui o `User` padrão do Django (`AUTH_USER_MODEL`). O campo de identificação é `cpf` (11 dígitos, sem formatação no banco), não `username` ou `email`.

**Fluxo de autenticação:**
1. `POST /api/autenticacao/registrar/` → valida CPF (dígitos verificadores), valida senha robusta, cria `Usuario`, retorna `Token`
2. `POST /api/autenticacao/login/` → autentica por CPF + senha, retorna `Token`

O token retornado deve ser enviado no header `Authorization: Token <token>` nas requisições autenticadas.

**Validações de senha** (`autenticacao/validators.py` + `SenhaRobustaValidator` em `AUTH_PASSWORD_VALIDATORS`): mínimo 8 caracteres, obrigatório maiúscula, minúscula, número e símbolo especial.

**Endpoint de health check:** `GET /api/test/` — retorna `{"status": "conectado"}`.

**CORS:** `CORS_ALLOW_ALL_ORIGINS = True` (dev only — restringir em produção).

**Banco:** SQLite em desenvolvimento (`db.sqlite3` ignorado pelo git via `.dockerignore`).

### Frontend (`frontend/`)

Quasar 2 (Vue 3 Composition API, Vite, Vue Router com hash mode).

- **`src/pages/`** — `LoginPage.vue`, `RegisterPage.vue`, `IndexPage.vue`, `ErrorNotFound.vue`
- **`src/layouts/`** — `MainLayout.vue` (layout das páginas autenticadas)
- **`src/router/routes.js`** — `/login` e `/registrar` são rotas sem layout; `/` usa `MainLayout`
- **`src/boot/`** — arquivos de boot do Quasar (plugins globais, axios config, etc.)
- **`src/css/app.scss`** — estilos globais; `quasar.variables.scss` para override de variáveis do Quasar

**Comunicação com API:** axios com URL hardcoded `http://localhost:8000` nas páginas (a ser centralizada em um boot file de axios). O token é armazenado em `localStorage`.

**CPF no frontend:** os inputs usam `mask="###.###.###-##"` com `unmasked-value`, portanto o valor em `v-model` já chega sem formatação (11 dígitos puros) — consistente com o que o backend espera.

### Docker

- `backend/Dockerfile` — Python 3.12-slim, instala dependências com `uv sync --frozen`
- `frontend/Dockerfile` — Node 22-slim, instala dependências com `pnpm` via corepack
- `docker-compose.yml` — orquestra os dois serviços; o volume anônimo `/app/node_modules` no frontend preserva os binários compilados para Linux dentro do container
- `devServer.host: '0.0.0.0'` no `quasar.config.js` é necessário para o Quasar ser acessível fora do container Docker

## Key Conventions

- Código e nomes de variáveis em **português** (cpf, senha, criado_em, carregando, etc.)
- Serializers usam campos `senha`/`confirmar_senha` (não `password`/`password2`)
- CPF é sempre normalizado para 11 dígitos numéricos antes de persistir ou autenticar
- Novos apps Django devem registrar o modelo em `INSTALLED_APPS` e criar migrations antes de rodar
