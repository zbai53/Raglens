"""RagLens FastAPI application entrypoint.

W1 D1 scope: minimal FastAPI app with /health.
Routers, middleware, and worker startup are wired up on D4.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__

logger = logging.getLogger("raglens.backend")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown hooks. Storage clients and ingest worker land D3/D4."""
    logger.info("raglens-backend %s starting", __version__)
    yield
    logger.info("raglens-backend %s shutting down", __version__)


app = FastAPI(
    title="RagLens Backend",
    version=__version__,
    description="Trace ingest, query, attribution, eval, and experiment APIs.",
    lifespan=lifespan,
)

# CORS: open in dev, tightened via env on D4.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Liveness probe. Used by docker-compose healthcheck and k8s later."""
    return {"status": "ok", "version": __version__}
