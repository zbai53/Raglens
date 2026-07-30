# PROGRESS.md — RagLens

> Living session log. Read at the start of every session, updated at the end.

---

## Current status

- **Phase**: Phase 1 — SDK + basic ingest
- **Week**: W1 — in progress
- **Overall**: 1/60 days
- **Last session**: 2026-07-29 (Day 1)

---

## Milestones

- [ ] W1: repo scaffold, data model, docker-compose all services up
- [ ] W2: Python SDK v0.1 — collect events, batch upload
- [ ] W3: backend ingest pipeline + trace list page
- [ ] W4: trace detail page (tree + timeline)
- [ ] W5: retrieval/generation specialized views
- [ ] W6: metrics dashboard + 3 official integrations
- [ ] W7: attribution (Level 1 + Level 2)
- [ ] W8: vector-space viz (UMAP + D3)
- [ ] W9: evaluation framework (4 RAGAS metrics)
- [ ] W10: A/B experiments + CI
- [ ] W11: polish, docs, demo video
- [ ] W12: release + iteration

---

## Key metrics

| Metric | Target | Current | Updated |
|---|---|---|---|
| SDK P99 added latency | < 5 ms | — | — |
| Backend single-instance ingest | 5000 event/s | — | — |
| Trace list P99 query | < 500 ms | — | — |
| UMAP 500-point layout + render | < 3 s | — | — |
| GitHub stars | ≥ 200 | 0 | — |
| PyPI downloads/month | ≥ 500 | 0 | — |

---

## Session log

### 2026-07-29 (W1 D1)

**Task**: `PROMPTS/week_01.md` → Day 1 (repo skeleton + docker-compose)

**Done**:
- [x] [infra] GitHub repo `zbai53/Raglens` created (Apache-2.0, public)
- [x] [infra] Vision `README.md` (v0.1) — value prop, comparison table vs LangSmith/Langfuse, ASCII architecture, roadmap
- [x] [infra] Monorepo `.gitignore` (Python + Node + Docker + editor + OS)
- [x] [infra] Monorepo directory scaffold: `sdk/`, `backend/`, `frontend/`, `docs/`, `examples/`, `docker/`
- [x] [infra] `docker-compose.yml` — 6 services (ClickHouse, Postgres, Redis, Qdrant, backend, frontend) with healthchecks + named volumes + `depends_on: service_healthy`
- [x] [infra] `docker/clickhouse-init/01_create_database.sql` — creates `raglens` DB on first boot
- [x] [infra] `.env.example` — full env variable list
- [x] [infra] `Makefile` — dev / up / down / lint / test / *-install / *-run / sdk-build
- [x] [backend] `pyproject.toml` (uv, Python 3.11, ruff/black/mypy strict) + full dep set (fastapi, sqlalchemy async, asynch, redis, qdrant, umap, anthropic, tenacity)
- [x] [backend] Multi-stage `Dockerfile` (builder w/ uv, runtime slim, non-root user)
- [x] [backend] `app/main.py` — FastAPI app + `/health` endpoint + CORS + lifespan hook
- [x] [backend] `tests/test_health.py` — smoke test
- [x] [sdk] `pyproject.toml` (hatchling, Python 3.9+, only `httpx` + `pydantic` deps)
- [x] [sdk] `src/raglens/__init__.py` — exports `__version__` only
- [x] [sdk] `tests/test_smoke.py`
- [x] [frontend] `Dockerfile` (multi-stage, standalone output, node:20-alpine, pnpm)
- [x] [frontend] `SETUP.md` — one-time bootstrap steps (`create-next-app@14.2`, deps, shadcn init)
- [x] [docs] `ARCHITECTURE.md` placeholder mirroring the project knowledge doc

**Not done / blocked**:
- [ ] `frontend/` real Next.js scaffold — deferred to when bai runs `pnpm create next-app` (see `frontend/SETUP.md`); Dockerfile is ready
- [ ] `docker compose up -d` end-to-end verification — needs frontend scaffold + first `uv sync` in backend
- [ ] CI (GitHub Actions) — moved to D2 (does not block D2 data-model work)

**Pitfalls encountered**:
- macOS Finder blocked dragging a dot-file (`.gitignore`) → resolved via `⌘+Shift+.` toggle, but afterwards discovered the committed `.gitignore` was still GitHub's default Python-only template (README got overwritten, .gitignore did not) → fixed by writing full monorepo version and committing separately.
- `git commit` errored on `.git/index.lock` — a background git process had crashed / been interrupted → `rm .git/index.lock` and retry.

**Decisions**:
- **Python packaging**: `uv` for both backend and SDK (chosen over pip-tools + requirements.txt). Rationale: 10-100× faster resolve/install, single-file `uv.lock`, and it's a legit interview talking point about modern tooling.
- **Ingest worker**: asyncio task inside the FastAPI process for W1-W8. Deferring Celery until W9 (batch eval runs justify the broker overhead). Rationale: minus one component, minus one failure mode, still meets 5000 event/s target.
- **Next.js version**: pinned to 14.2 + React 18 (not Next 15 + React 19). Rationale: shadcn/tanstack-query/react-flow ecosystem is fully compatible on 14/18; 15/19 still has rough edges.
- **License**: Apache 2.0 (matches Langfuse/LangSmith positioning; permissive enough for enterprise adoption).
- **Repo visibility**: public from day 1 (start accruing baseline star history early; nothing sensitive in a scaffold).

**Next**:
- W1 D2 — Alembic + PostgreSQL models (Project, Dataset, EvalRun, Experiment) + all Pydantic schemas
- Before D2: run `frontend/SETUP.md` steps, `docker compose up -d`, verify 6 services healthy

**Commits**:
- `1e37504  chore(repo): initial scaffold with vision README, Apache-2.0, and monorepo .gitignore`
- `4e74748  chore(repo): expand .gitignore to cover Node/Docker/OS/editor artifacts`
- `de4e7f4  chore(infra): scaffold docker-compose 6 services, env.example, Makefile`
- `fbb100b  feat(backend): FastAPI /health skeleton, uv pyproject, multi-stage Dockerfile`
- `cead796  feat(sdk): v0.0.1 skeleton — hatchling, httpx+pydantic deps only`
- `07da18a  chore(frontend): Dockerfile for Next 14 standalone + SETUP.md bootstrap`
- `7444a6b  docs: PROGRESS.md D1 log, ARCHITECTURE.md placeholder, subdir READMEs`

---

## Blockers / risks

| Date | Risk / blocker | Status | Mitigation |
|---|---|---|---|
| — | — | — | — |

---

## Key learnings & technical insights

> Interview goldmine — populate as things happen.

### SDK design
- _(TBD, W2+)_

### ClickHouse
- _(TBD, W3)_

### Vector viz
- _(TBD, W8)_

### Attribution
- _(TBD, W7)_

### Evaluation
- _(TBD, W9)_

---

## Scope change log

- _(none yet)_
