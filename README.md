<div align="center">
    <h1>💬 RS-MIV-1</h1>
    <p>
        <b>Rede Social de Mensagens Instantâneas em Vue.js</b>
    </p>
</div>

## Visão geral

O RS-MIV (Rede Social de Mensagens Instantâneas em Vue.js) é uma aplicação de chat em tempo real via mensagens de texto, construída como projeto de portfólio. Hoje, a aplicação está implantada em produção (Render, Neon e Upstash), e atualmente se encontra na fase final de desenvolvimento.

Tive como objetivos me aprofundar no uso de Vue.js e TypeScript para desenvolvimento front-end - escolhendo Python para o back-end por familiaridade com a linguagem, mas curiosidade de fazer uma API com ela - e obter conhecimento num protocolo de *instant messaging* (comunicação instantânea), que nesse caso foi o WebSocket (RFC 6455).

Ao longo do desenvolvimento, o escopo se expandiu para incluir persistência de mensagens em PostgreSQL e Redis, criptografia end-to-end através de pares de chaves PGP e o uso do Alembic para permitir migração do banco de dados — tornando o projeto um estudo mais aprofundado de segurança e arquitetura full-stack do que antes planejado. 

## Estrutura de arquivos

O projeto é organizado numa estrutura monólita (monorepo), contendo tanto o código para execução da API quanto do website.

```
rs-miv-1/
├── backend/
│   ├── alembic/            # Migrations versionadas
│   ├── app/
│   │   ├── conn/           # Configuração de conexões externas (engine, get_db)
│   │   ├── dependencies/   # Dependências injetáveis nos endpoints (ex.: get_current_user)
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── repositories/   # Acesso a dados (padrão Repository, funções assíncronas)
│   │   ├── routers/        # Endpoints da API (REST + WebSocket)
│   │   ├── schemas/        # Schemas Pydantic (validação e serialização)
│   │   └── utils/          # Funções utilitárias (validação, criptografia, etc.)
│   ├── main.py             # Entry point da aplicação FastAPI
│   ├── docker-compose.yml  # Ambiente local (Postgres + Redis)
│   ├── requirements.txt
│   └── start.sh            # Executa migrations + inicia o servidor
│
├── docs/                   # Documentação adicional (roadmaps, wireframes, etc.)
└── frontend/
    ├── src/
    │   ├── api/            # Chamadas HTTP à API
    │   ├── assets/
    │   ├── components/     # Componentes Vue
    │   ├── composables/    # Lógica reativa reutilizável (useAuth, useWebSocket, etc.)
    │   ├── router/         # Vue Router
    │   ├── utils/          # Funções utilitárias sem estado reativo
    │   ├── views/          # Páginas/rotas
    │   ├── App.vue
    │   └── main.ts         # Ponto de inicialização do site estático
    ├── env.d.ts            # Tipagem global (Vite, PGP, IDs, payloads da API)
    ├── package.json
    └── vite.config.ts      # Configuração do Vite
```

## Tecnologias e ferramentas

### Back-end

- **FastAPI** — framework Python assíncrono para os endpoints REST e o servidor WebSocket
- **SQLAlchemy 2.x (async)** + **Alembic** — ORM e versionamento de schema
- **PostgreSQL** — persistência principal
- **Redis** — presença de usuários e cache de mensagens recentes
- **`python-jose`** — emissão e validação de JWT
- **`pwdlib[bcrypt]`** — hashing de senhas
- **`cryptography`** — derivação da chave de sessão simétrica (HKDF)
- **PGPy** — operações PGP no lado do servidor

### Front-end

- **Vue 3** + **TypeScript** — composição reativa e tipagem estática
- **Tailwind CSS** — estilização utilitária
- **Vue Router** — navegação
- **`openpgp.js`** (v6, Curve25519) — geração de par de chaves e criptografia E2E no cliente
- **DOMPurify** — sanitização de conteúdo renderizado

### Infraestrutura

- **Docker Compose** — ambiente de desenvolvimento local (Postgres + Redis)
- **Render** — hospedagem do back-end e do front-end estático
- **Neon** — PostgreSQL gerenciado em produção
- **Upstash** — Redis gerenciado em produção 

## Arquitetura

Considerando o peso significativo que as decisões de segurança - sanitização de mensagens e criptografia end-to-end (E2E) - deram ao resultado final do projeto, ambas sendo grande fonte de aprendizado, as colocarei como seções separadas das demais decisões arquiteturais e seus trade-offs.

### Criptografia E2E

(T.B.D)

### Sanitização de mensagens

(T.B.D)

### Outras decisões de design e trade-offs

(T.B.D)

## Como executar localmente

### Front-end

No caso do front-end, todas as variáveis de ambiente são públicas e já estão definidas. Atualmente, para desenvolvimento local, elas são:

```env
VITE_API_URL=http://localhost:8000  # URL usado para fazer requisições HTTP
VITE_WS_URL=ws://localhost:8000     # URL usado para fazer entrar no WebSocket
PAGE_TITLE="RS-MIV"                 # Título-base das páginas do site
```

Para instalar as dependências do projeto:

```sh
npm install
```

Após isso, para executar o projeto em um servidor de desenvolvimento (com Vue DevTools nativo):

```sh
npm run dev
```

Caso deseje compilar e compactar o projeto para produção, há duas opções:

```sh
# Com type-checking embutido (RECOMENDADO):
npm run build

# Ou, sem type-checking:
npm run build-only
```

Para mais informações sobre o Vite, ler o [`README.md`](./frontend/README.md) específico da pasta `frontend/`, ou a lista de scripts em [`package.json`](./frontend/package.json).

### Back-end (API RESTful)

> [!IMPORTANT] 
> Antes de tentar executar o back-end, certifique-se que os bancos de dados já estão funcionando - seja localmente (via Docker Compose) ou remotamente - **se não, a API não inicializará**. 
>
> Caso deseja seguir com a execução local, veja a seção seguinte: [Bancos de dados (PostgreSQL & Redis)](#bancos-de-dados-postgresql--redis)

Antes de tudo, crie um arquivo `.env` na raiz da pasta `backend/` contendo os seguintes valores abaixo.

```env # Só pra ter highlight de cores mesmo
# --- URLs secretas ---
# Os valores das URLs podem ser substituídos conforme o que você for usar, mas aqui
# já está os padrões conforme o docker-compose.yml e às configurações do front-end:
REDIS_URL="redis://localhost:6379"
DB_URL="postgresql://rsmiv:rsmiv_dev_password@localhost:5432/rsmiv_dev" 
CORS_ALLOWED_ORIGINS="http://localhost:5173" # Pode ser uma lista de endereços separada por vírgulas, sem espaços (ex.: "http://a.a,http://b.b")

# --- Variáveis de controle ---
DB_ECHO=['True' ou 1 | 'False' ou 0] # Determina se as queries do banco SQL devem ser logadas ou não

# --- Chaves secretas ---
JWT_SECRET_KEY=[insira chave secreta AES-256]
SESSION_KEY_SEED=[insira chave secreta AES-256]
```

Antes de instalar os pacotes, é recomendado criar um ambiente virtual Python (venv) isolado na pasta `backend/`, com o comando abaixo:

```sh
python -m venv .venv
```

Em seguida, realize a instalação dos pacotes versionados listados em `requirements.txt`.

```sh
pip install -r requirements.txt
```

Após isso, você está livre para inicializar o servidor de desenvolvimento Uvicorn.

```sh
# Verifica se é necessário uma migration antes de rodar a API:
sh start.sh

# Mesmas opções de "start.sh", mas sem migration:
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Opção mais simples, com reload da API ao mudar código (RECOMENDADO PARA TESTES): 
uvicorn app.main:app --reload
```

### Bancos de dados (PostgreSQL & Redis)

O guia a seguir é para a integração dos bancos de dados como serviços em contêineres Docker (método recomendado). Caso desejar continuar usando serviços remotos (ex.: Upstash ou Redis Cloud p/a Redis; Neon ou Supabase p/a banco relacional) ou outros serviços locais já configurados, apenas altere as duas variáveis de ambiente abaixo em `backend/.env`: 

```env
DB_URL=[nova URL]
REDIS_URL=[nova URL]
```

Caso deseja prosseguir com a execução padrão, certifique-se o Docker está instalado e configurado (com o Docker Compose) na sua máquina.

Como a pasta `backend/` já contêm um arquivo `docker-compose.yml`, iremos utilizar as configurações nele estabelecidas para baixar as imagens e iniciar os serviços `backend-postgres-1` e `rs-miv-1-redis`.

```sh
docker compose up -d

# Ou, inicie cada serviço separadamente:
docker compose up backend-postgres-1
docker compose up rs-miv-1-redis
```

Cada um dos serviços há algum tipo de CLI que pode ser executada, permitindo visualização e interação com os dados diretamente, sem intermédio da API.

Para abrir a `redis-cli`, execute o seguinte comando:

```sh
docker exec -it rs-miv-1-redis redis-cli
```

Para abrir o PostgreSQL via `psql` no terminal, dentro do próprio contêiner, execute o seguinte comando:

```sh
docker compose exec postgres psql -U rsmiv -d rsmiv_dev
# Senha não é necessária pois conexões de dentro do contêiner são tidas como confiáveis
```
Você pode substituir `rsmiv` por outro nome de usuário e `rsmiv_dev` por outro banco de dados, caso alterar os valores correspondentes (`POSTGRES_USER` e `POSTGRES_DB`) em `docker-compose.yml`.

## Roadmap

### Fases Concluídas

(T.B.D)

### Estado Atual

(T.B.D)

### Próximos Passos

(T.B.D)

## Limitações Conhecidas

(T.B.D)

## Agradecimentos

(T.B.D)
