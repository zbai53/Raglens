# RagLens developer shortcuts.
# Run `make help` to see targets.

.PHONY: help dev up down logs ps clean \
        backend-install backend-lint backend-fmt backend-test backend-run \
        sdk-install sdk-lint sdk-test sdk-build \
        frontend-install frontend-lint frontend-test frontend-run \
        lint test

# ---------------------------------------------------------------------------
# Meta
# ---------------------------------------------------------------------------
help:  ## Show this help
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ---------------------------------------------------------------------------
# Docker compose
# ---------------------------------------------------------------------------
dev: up  ## Alias for `up`

up:  ## Start all services in background
	docker compose up -d
	@echo "Backend:  http://localhost:8000/docs"
	@echo "Frontend: http://localhost:3000"

down:  ## Stop and remove containers
	docker compose down

logs:  ## Tail logs from all services
	docker compose logs -f

ps:  ## List service status
	docker compose ps

clean:  ## Stop containers and delete volumes (DESTROYS DATA)
	docker compose down -v

# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------
backend-install:  ## Install backend deps (uv)
	cd backend && uv sync --all-extras

backend-lint:  ## Lint backend (ruff + mypy)
	cd backend && uv run ruff check app tests
	cd backend && uv run mypy app

backend-fmt:  ## Format backend (black + ruff --fix)
	cd backend && uv run black app tests
	cd backend && uv run ruff check --fix app tests

backend-test:  ## Run backend pytest
	cd backend && uv run pytest

backend-run:  ## Run backend locally (uvicorn)
	cd backend && uv run uvicorn app.main:app --reload --port 8000

# ---------------------------------------------------------------------------
# SDK
# ---------------------------------------------------------------------------
sdk-install:  ## Install SDK deps (uv)
	cd sdk && uv sync --all-extras

sdk-lint:  ## Lint SDK
	cd sdk && uv run ruff check src tests
	cd sdk && uv run mypy src

sdk-test:  ## Run SDK pytest
	cd sdk && uv run pytest

sdk-build:  ## Build SDK wheel + sdist
	cd sdk && uv build

# ---------------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------------
frontend-install:  ## Install frontend deps (pnpm)
	cd frontend && pnpm install

frontend-lint:  ## Lint frontend (tsc + biome/eslint if configured)
	cd frontend && pnpm exec tsc --noEmit

frontend-test:  ## Run frontend tests (Playwright)
	cd frontend && pnpm exec playwright test

frontend-run:  ## Run frontend dev server
	cd frontend && pnpm dev

# ---------------------------------------------------------------------------
# Aggregates
# ---------------------------------------------------------------------------
lint: backend-lint sdk-lint frontend-lint  ## Lint everything

test: backend-test sdk-test  ## Run all unit tests (frontend E2E via `make frontend-test`)
