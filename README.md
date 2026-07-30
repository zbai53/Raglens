# RagLens

> **Chrome DevTools for RAG.** Open-source observability for Retrieval-Augmented Generation applications — trace every step, attribute every answer, visualize your vector space, and evaluate with reproducible metrics.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

---

## Why RagLens

Debugging a RAG pipeline today means `print()`, log spelunking, and eyeballing chunks. RagLens gives you:

- **End-to-end trace** — every embedding, retrieval, rerank, and generation call captured with 3 lines of SDK code.
- **Answer attribution** — see which chunks each sentence of your answer actually came from (embedding-based, or LLM-judged on demand).
- **Vector-space explorer** — UMAP projection of your query against retrieved chunks. Instantly spot "why didn't the right chunk get retrieved?"
- **Reproducible eval** — 4 built-in RAGAS metrics (faithfulness, context precision/recall, answer relevancy), dataset management, and A/B experiments you can wire into CI.
- **Self-hostable** — one `docker compose up`. No vendor lock-in, no data leaves your infra.

## How it compares

| | RagLens | LangSmith | Langfuse |
|---|---|---|---|
| Open-source | ✅ Apache 2.0 | ❌ | ✅ |
| Self-host | ✅ | ❌ | ✅ |
| Vector-space viz | ✅ | ❌ | ❌ |
| Answer attribution | ✅ | ❌ | Partial |
| RAG-specialized | ✅ | General LLM | General LLM |
| Chinese LLM judges (DeepSeek/Qwen) | ✅ first-class | ❌ | ❌ |

## Architecture

```
   ┌────────────┐   3 lines    ┌─────────────┐   batch     ┌──────────────┐
   │  Your RAG  │─────────────▶│  raglens    │────────────▶│   Ingest     │
   │    app     │   (async,    │  Python SDK │   HTTP+gzip │   FastAPI    │
   └────────────┘   non-blocking)└─────────────┘             └──────┬───────┘
                                                                    │
                                                                    ▼
                                                             ┌──────────────┐
                                                             │ Redis Streams│  buffer
                                                             └──────┬───────┘
                                                                    ▼
        ┌───────────────┐        ┌─────────────┐         ┌──────────────┐
        │  Next.js UI   │◀───────│  Query API  │◀────────│  ClickHouse  │  traces/events
        │  React + D3   │        │   FastAPI   │         │  + Postgres  │  metadata
        └───────────────┘        └─────────────┘         └──────────────┘
```

Full design: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Quickstart

> **Alpha — not production yet.** Week 1 goal: `docker compose up` runs the full stack locally.

```bash
git clone https://github.com/<you>/raglens.git
cd raglens
cp .env.example .env
docker compose up -d
# Frontend:  http://localhost:3000
# API docs:  http://localhost:8000/docs
```

Once services are up:

```python
# 3-line integration (available week 2)
from raglens import RAGTrace

tracer = RAGTrace(api_key="rl_...", project="my-rag-app")

with tracer.trace(query="what is RAG?") as t:
    chunks = retriever.get_relevant_documents("what is RAG?")
    t.log_retrieval(chunks)
    answer = llm.invoke(build_prompt(chunks))
    t.log_generation(answer)
```

## Roadmap

12-week build to first release. Full plan: [`docs/ROADMAP.md`](docs/ROADMAP.md).

| Phase | Weeks | Deliverable |
|---|---|---|
| SDK + ingest | W1–W3 | End-to-end: SDK → API → ClickHouse → UI list |
| Trace visualization | W4–W6 | Trace tree, retrieval/generation views, metrics dashboard |
| Attribution + vector space | W7–W8 | Answer attribution, UMAP explorer |
| Eval + A/B | W9–W10 | 4 RAGAS metrics, experiments, CI integration |
| Ship | W11–W12 | Docs, demo video, public launch |

## Status

**Current week**: W1 — repo scaffold + docker-compose + data models.
Progress log: [`docs/PROGRESS.md`](docs/PROGRESS.md).

## Contributing

Repo is public from day one, but the API is unstable until v0.1.0. Watch/star to follow along. Contribution guide coming with v0.1.

## License

Apache 2.0 — see [LICENSE](LICENSE).
