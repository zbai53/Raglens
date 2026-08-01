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
- [ ] CI (GitHub Actions) — moved to D2 (does not block D2 data-model work)

**Pitfalls encountered**:
- **macOS Finder blocks dragging dot-files** — `.gitignore` didn't drag in; fixed with `⌘+Shift+.` to show hidden files. Also discovered committed `.gitignore` was still GitHub's default Python-only template (README overwrote, .gitignore didn't). Fixed by rewriting the full monorepo version.
- **`.git/index.lock` reappeared after every commit** — cause: an IDE/GUI (VS Code / Fork / Warp starship prompt) was auto-running `git status` in the background and racing with terminal git. Workaround: `rm -f .git/index.lock` before commit. Real fix: disable auto-fetch in IDE for high-frequency commit workflows.
- **hatchling + docker `.dockerignore *.md` collision** — hatchling validates the `readme` metadata field during `build_editable` by opening `README.md`. If `.dockerignore` excludes it, the whole `uv sync` chain fails cryptically ("Failed to fetch wheel: raglens-backend @ file:///app"). Fix: `!README.md` exception + explicit `COPY README.md` in Dockerfile. **Interview point**: PEP 517 build isolation runs in a tempdir that only sees files declared in the source tree — this is how you learn *what* your `pyproject.toml` actually depends on.
- **`create-next-app@14.2` no longer scaffolds `public/`** when the directory would be empty; Dockerfile `COPY /app/public` then fails cache-key computation. Fix: `public/.gitkeep`.
- **`clickhouse/clickhouse-server:24-alpine` unhealthy on Apple Silicon** — the `-alpine` variant has musl/jemalloc/lz4 issues on arm64. Fix: switch to debian-based `clickhouse/clickhouse-server:24.8`. Also wiped stale volume (`docker volume rm raglens_clickhouse_data raglens_clickhouse_logs`) before restart. **Interview point**: when picking DB images for local dev, alpine ≠ automatically smaller/better; jemalloc-based systems (ClickHouse, MongoDB, ScyllaDB) tend to be more stable on glibc.
- **frontend healthcheck failed but service was actually ready** — used `wget --spider` on node:20-alpine; BusyBox wget's exit code semantics disagreed with health-check assumptions. Fix: switch to node built-in `require('http').get()` — no external tool needed, uses the same runtime as the app, and works uniformly across alpine/debian.
- **`SHOW DATABASES` returned "Authentication failed"** — when compose sets `CLICKHOUSE_USER=raglens`, the `default` user is disabled. `curl` without `-u raglens:raglens` hits the default user and fails. Not a bug, but easy to mistake for one during verification.

**Decisions**:
- **Python packaging**: `uv` for both backend and SDK (chosen over pip-tools + requirements.txt). Rationale: 10-100× faster resolve/install, single-file `uv.lock`, and it's a legit interview talking point about modern tooling.
- **Ingest worker**: asyncio task inside the FastAPI process for W1-W8. Deferring Celery until W9 (batch eval runs justify the broker overhead). Rationale: minus one component, minus one failure mode, still meets 5000 event/s target.
- **Next.js version**: pinned to 14.2 + React 18 (not Next 15 + React 19). Rationale: shadcn/tanstack-query/react-flow ecosystem is fully compatible on 14/18; 15/19 still has rough edges.
- **License**: Apache 2.0 (matches Langfuse/LangSmith positioning; permissive enough for enterprise adoption).
- **Repo visibility**: public from day 1 (start accruing baseline star history early; nothing sensitive in a scaffold).

**Verified end-to-end** (D1 acceptance):
- `docker compose ps` → all 6 services healthy
- `curl localhost:8000/health` → `{"status":"ok","version":"0.0.1"}`
- `curl -u raglens:raglens "localhost:8123/?query=SHOW+DATABASES"` → includes `raglens`
- `curl -sI localhost:3000` → `HTTP/1.1 200 OK`
- `curl localhost:8000/docs` → Swagger HTML

**Next**:
- W1 D2 — Alembic + PostgreSQL models (Project, Dataset, EvalRun, Experiment) + all Pydantic schemas + Swagger showing all schema definitions

**Commits**:
- `1e37504  chore(repo): initial scaffold with vision README, Apache-2.0, and monorepo .gitignore`
- `4e74748  chore(repo): expand .gitignore to cover Node/Docker/OS/editor artifacts`
- `de4e7f4  chore(infra): scaffold docker-compose 6 services, env.example, Makefile`
- `fbb100b  feat(backend): FastAPI /health skeleton, uv pyproject, multi-stage Dockerfile`
- `cead796  feat(sdk): v0.0.1 skeleton — hatchling, httpx+pydantic deps only`
- `07da18a  chore(frontend): Dockerfile for Next 14 standalone + SETUP.md bootstrap`
- `10d927e  docs: PROGRESS.md D1 log, ARCHITECTURE.md placeholder, subdir READMEs`
- `3f218a7  feat(frontend): Next.js 14 scaffold with Tailwind, shadcn/ui (Radix), and RagLens deps (zustand/tanstack/d3/reactflow/recharts)`
- `adf52e8  fix(backend): allow README.md in docker build (hatchling requires readme file to exist)`
- `b3d9373  fix(frontend): add public/ dir (create-next-app 14.2 skips it when empty)`
- `793b6ee  fix(infra): use debian ClickHouse image on arm64, switch frontend healthcheck to node http`
- `bf97f36  docs: PROGRESS.md D1 completion — 6 pitfalls, D1 acceptance verified`

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
