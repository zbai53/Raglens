"""Pydantic schema re-exports.

Kept flat so imports read `from app.schemas import TraceCreate, ProjectResponse`
instead of `from app.schemas.trace import TraceCreate`.
"""

from app.schemas.attribution import Attribution, AttributionSource
from app.schemas.common import EventKind, TraceStatus
from app.schemas.dataset import DatasetCreate, DatasetResponse, EvalItem
from app.schemas.experiment import ExperimentConfig, ExperimentCreate, ExperimentResult
from app.schemas.project import ProjectCreate, ProjectResponse
from app.schemas.trace import (
    Chunk,
    EmbeddingEvent,
    Event,
    GenerationEvent,
    RetrievalEvent,
    Trace,
    TraceCreate,
    TraceIngestBatch,
)

__all__ = [
    # common
    "EventKind",
    "TraceStatus",
    # trace
    "Chunk",
    "Event",
    "EmbeddingEvent",
    "RetrievalEvent",
    "GenerationEvent",
    "Trace",
    "TraceCreate",
    "TraceIngestBatch",
    # project
    "ProjectCreate",
    "ProjectResponse",
    # dataset
    "EvalItem",
    "DatasetCreate",
    "DatasetResponse",
    # attribution
    "Attribution",
    "AttributionSource",
    # experiment
    "ExperimentConfig",
    "ExperimentCreate",
    "ExperimentResult",
]
