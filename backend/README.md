# backend

FastAPI application: trace ingest, query, eval, attribution, vector-space APIs.

## Stack

- **Runtime**: Python 3.11, FastAPI, uvicorn
- **Package manager**: [uv](https://github.com/astral-sh/uv)
- **Storage**: ClickHouse (traces/events), PostgreSQL (metadata), Redis (streams + cache), Qdrant (embedding index)
- **Async worker**: asyncio task consuming Redis Streams → batch INSERT ClickHouse
- **Lint/format**: ruff, black, mypy (strict)

## Dev

```bash
cd backend
uv sync                    # install deps into .venv
uv run uvicorn app.main:app --reload --port 8000
```

Or via docker-compose from repo root:

```bash
docker compose up backend
```

Swagger: <http://localhost:8000/docs>
