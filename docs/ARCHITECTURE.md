# Architecture

> Placeholder. Full design lives in the project knowledge doc; this file will mirror it and stay in sync with the code.

## System overview

```
User RAG app → raglens SDK → HTTP batch → Backend Ingest API
                                                ↓
                                         Redis Streams (buffer)
                                                ↓
                                     Ingest Worker (asyncio task)
                                                ↓
                                          ClickHouse (traces + events)

                          Postgres (metadata: projects, datasets, eval, experiments)
                          Qdrant   (embedding index, W7+)

Frontend (Next.js) ↔ Backend Query API ↔ ClickHouse / Postgres / Qdrant
```

## Storage responsibilities

| Store | Owns | Access pattern |
|---|---|---|
| ClickHouse | traces, events, hourly aggregates | high-throughput write, analytical read |
| PostgreSQL | projects, api keys, datasets, eval runs, experiments | OLTP CRUD |
| Redis | ingest stream, query cache, UMAP layout cache | ephemeral, TTL |
| Qdrant | embedding index for vector-space viz (W7+) | ANN search |

## Service boundaries

- **SDK** — user-facing library. Zero external deps beyond `httpx` + `pydantic`. Never blocks user code.
- **Backend** — FastAPI monolith with async worker in the same process (W1). May split into ingest/query/worker later if load demands.
- **Frontend** — Next.js App Router. All data via the backend's REST API.

## Details to fill in (per week)

- W3: full ingest pipeline + ClickHouse DDL + query API
- W4-6: trace visualization + retrieval/generation views
- W7: attribution service (embedding + LLM-judge)
- W8: UMAP layout service + caching
- W9: eval framework (RAGAS metrics)
- W10: experiments + CI integration
