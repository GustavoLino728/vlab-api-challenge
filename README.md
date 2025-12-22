# VLab API Challenge – Abastecimentos

API REST construída em **FastAPI** para ingestão e consulta de abastecimentos, com:

- Validação de **CPF** de motorista.  
- Cálculo de flag de **anomalia** em abastecimentos (preço fora da média).  
- Persistência em **PostgreSQL** via SQLAlchemy + Alembic.  
- Autenticação por **API Key** no endpoint de ingestão.  
- Endpoint de **health check**.  
- Testes automatizados com **pytest**.  
- Padronização de código com **Black**.  

## Tecnologias

- **Python 3.11**  
- **FastAPI** + **Uvicorn**  
- **PostgreSQL 16**  
- **SQLAlchemy** + **Alembic**  
- **Pydantic v2**  
- **Pytest**  
- **Black** (formatação de código)
- **Docker** + **Docker Compose**


## Como rodar o projeto

### 1. Pré‑requisitos

- Docker e Docker Compose instalados.

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (a partir de `.env.example`, se existir), por exemplo:

```env
DATABASE_URL=postgresql+asyncpg://vlab:vlab@db:5432/vlab
DATABASE_URL_SYNC=postgresql+psycopg2://vlab:vlab@db:5432/vlab

API_KEY=supersecret
POSTGRES_USER=vlab
POSTGRES_PASSWORD=vlab
POSTGRES_DB=vlab
```

- `API_KEY` será usada para autenticar o endpoint de ingestão.  

### 3. Subir containers

```bash
docker compose up --build
```

Isso sobe:

- `vlab_api`: API FastAPI rodando em `http://localhost:8000`.  
- `vlab_db`: banco PostgreSQL.  
- (Opcional) `load_data`: script que gera dados fakes e chama a API.  

## Documentação / Swagger

Após subir os containers:

- **Swagger UI**: `http://localhost:8000/docs`  
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`  

No Swagger, use o botão **Authorize** para informar a API Key (header `X-API-Key`) e testar o `POST /api/v1/abastecimentos`.

## Endpoints principais

### Health Check

- **Método**: `GET`  
- **Path**: `/api/v1/health`  
- **Autenticação**: pública  
- **Resposta (200)**:

```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": "up"
}
```

Esta rota executa um `SELECT 1` simples para verificar a conectividade com o banco.

### Abastecimentos

#### POST /api/v1/abastecimentos

- **Método**: `POST`  
- **Path**: `/api/v1/abastecimentos`  
- **Autenticação**: **API Key**  

Header obrigatório:

```http
X-API-Key: <valor de API_KEY do .env>
```

Exemplo de payload:

```json
{
  "id_posto": 1,
  "data_hora": "2025-01-01T10:30:00",
  "tipo_combustivel": "GASOLINA",
  "preco_por_litro": 5.79,
  "volume_abastecido": 40.5,
  "cpf_motorista": "13039523430"
}
```

Validações principais:

- CPF é normalizado e validado (remoção de pontuação e checagem dos dígitos).  
- `tipo_combustivel` aceita apenas valores pré‑definidos (ex.: `GASOLINA`, `ETANOL`, `DIESEL`).  
- Calcula uma flag de anomalia (`improper_data`) quando o preço por litro está acima de um limite (por exemplo, 25% acima da média estimada por tipo de combustível).  

Resposta (201 Created) retorna os dados do abastecimento persistido, incluindo a flag de anomalia.  

#### GET /api/v1/abastecimentos

- **Método**: `GET`  
- **Path**: `/api/v1/abastecimentos`  
- **Autenticação**: pública  
- Suporta paginação (schema `Page`) e filtros básicos de consulta (ajustar conforme os parâmetros implementados).  

## Autenticação via API Key

A autenticação é feita com um header simples:

- Header: `X-API-Key`  
- Valor: configurado em `API_KEY` no `.env` e lido pelo `Settings` (Pydantic Settings).

A dependência de segurança (`verify_api_key`) é aplicada:

- Somente no `POST /api/v1/abastecimentos`.  
- As demais rotas (GET, health, etc.) permanecem abertas.  

Fluxo típico:

1. O cliente obtém a chave (neste desafio, estática no `.env`).  
2. Envia em todas as requisições de ingestão:  

   ```http
   X-API-Key: supersecret
   ```

3. Se a chave estiver ausente ou incorreta, retorna `401 Unauthorized`.  

## Script de carga de dados (`load_data.py`)

O projeto inclui um script assíncrono que gera requisições de teste usando **Faker** e **httpx**:

- Gera CPFs válidos e dados aleatórios de abastecimento.  
- Dispara `NUM_REQUESTS` requisições `POST /api/v1/abastecimentos` com intervalo configurável.  

Pontos importantes:

- Lê a API Key do ambiente:

  ```py
  API_KEY = os.getenv("API_KEY", "changeme")
  headers = {"X-API-Key": API_KEY}
  ```

- Usa `httpx.AsyncClient` para enviar requisições em paralelo, com logs simples de sucesso/erro.

### Como rodar manualmente

Com containers rodando:

```bash
docker compose exec api python load_data.py
```

Ele roda automaticamente uma vez na subida.


## Testes Automatizados

Os testes utilizam **pytest**.

### Como rodar

Dentro do container da API:

```bash
docker compose exec api sh -c "cd /app && pytest -q"
```

Principais testes:

- **`tests/test_cpf.py`**  
  - Testa a função que remove caracteres não numéricos do CPF (`only_digits`).  
  - Testa a função de validação de CPF (`is_valid_cpf`) com um CPF válido e alguns inválidos (sequências repetidas, número aleatório).  

- **`tests/test_improper_data.py`**  
  - Testa a regra que define o campo `improper_data` com base na diferença percentual do preço em relação à média estimada por tipo de combustível.  
  - Verifica cenários onde o preço está dentro do limite e acima do limite.  

Todos os testes atuais passam (`5 passed`), com apenas um warning de depreciação do Pydantic relacionado a `config` de `BaseModel`.  

## Padronização de código (Black)

O projeto utiliza **Black** para formatação automática do código.

Arquivo `pyproject.toml` na raiz:

```toml
[tool.black]
line-length = 88
target-version = ["py311"]
```

### Rodar o formatador

No host:

```bash
black app tests load_data.py
```

Ou dentro do container:

```bash
docker compose exec api sh -c "cd /app && black app tests load_data.py"
```

Isso garante um estilo consistente de código em todo o projeto.  

## Estrutura do projeto (resumo)

```text
vlab-api-challenge/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── routes/
│   │           ├── abastecimentos.py
│   │           ├── motoristas.py
│   │           └── health.py
│   ├── core/
│   │   ├── config.py
│   │   └── db.py
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── utils/
│       └── cpf.py
├── tests/
│   ├── test_cpf.py
│   └── test_improper_data.py
├── load_data.py
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```