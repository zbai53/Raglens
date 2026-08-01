"""RagLens FastAPI application entrypoint.

W1 D1 scope: minimal FastAPI app with /health.
W1 D2 scope: schema stubs so Swagger surfaces them (real endpoints on D4).
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import settings
from app.schemas import (
    Attribution,
    DatasetCreate,
    DatasetResponse,
    ExperimentCreate,
    ExperimentResult,
    ProjectCreate,
    ProjectResponse,
    Trace,
    TraceIngestBatch,
)

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

# CORS is driven by settings; comma-separated origins in .env.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Meta
# ---------------------------------------------------------------------------
@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Liveness probe. Used by docker-compose healthcheck and k8s later."""
    return {"status": "ok", "version": __version__}


# ---------------------------------------------------------------------------
# D2 stub routers — real implementations land D4+.
# Purpose: force FastAPI to include the schemas in the generated OpenAPI so
# the frontend / docs can see them today.
# ---------------------------------------------------------------------------
stubs = APIRouter(prefix="/v1", tags=["stubs (D2 preview)"])


@stubs.post("/projects", response_model=ProjectResponse, status_code=501)
async def _stub_create_project(body: ProjectCreate) -> ProjectResponse:  # noqa: ARG001
    raise NotImplementedError("Implemented on W1 D4.")


@stubs.post("/traces/batch", status_code=501)
async def _stub_ingest_traces(body: TraceIngestBatch) -> dict[str, int]:  # noqa: ARG001
    raise NotImplementedError("Implemented on W1 D4.")


@stubs.get("/traces/{trace_id}", response_model=Trace, status_code=501)
async def _stub_get_trace(trace_id: str) -> Trace:  # noqa: ARG001
    raise NotImplementedError("Implemented on W1 D4.")


@stubs.post("/datasets", response_model=DatasetResponse, status_code=501)
async def _stub_create_dataset(body: DatasetCreate) -> DatasetResponse:  # noqa: ARG001
    raise NotImplementedError("Implemented on W3+.")


@stubs.post("/experiments", response_model=ExperimentResult, status_code=501)
async def _stub_create_experiment(body: ExperimentCreate) -> ExperimentResult:  # noqa: ARG001
    raise NotImplementedError("Implemented on W10.")


@stubs.get(
    "/traces/{trace_id}/attribution",
    response_model=list[Attribution],
    status_code=501,
)
async def _stub_get_attribution(trace_id: str) -> list[Attribution]:  # noqa: ARG001
    raise NotImplementedError("Implemented on W7.")


app.include_router(stubs)
