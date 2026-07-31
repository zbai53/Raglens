# Multi-stage build: uv-based dep resolution → slim runtime.
# ---------------------------------------------------------------------------
# Stage 1: builder — installs deps into a project-local .venv using uv
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# uv: fast dependency resolver + installer
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Install system deps needed to build psycopg / clickhouse-driver wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata first for better layer caching.
# README.md is required by hatchling for the `readme` metadata field.
COPY pyproject.toml uv.lock* README.md ./

# Install ONLY production deps into /app/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev || \
    uv sync --no-install-project --no-dev

# Copy the app source and install the project itself
COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev || uv sync --no-dev

# ---------------------------------------------------------------------------
# Stage 2: runtime — minimal image, no build toolchain
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
      libpq5 \
      curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app

# Bring over the venv and the app
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/app /app/app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
