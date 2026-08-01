"""Cross-schema enums and small types shared by multiple schemas."""

from __future__ import annotations

from enum import Enum


class EventKind(str, Enum):
    """Kind of pipeline step captured inside a trace.

    Kept as str-Enum so it serializes cleanly to JSON and stays stable across
    SDK and backend without needing a translation layer.
    """

    EMBEDDING = "embedding"
    RETRIEVAL = "retrieval"
    RERANK = "rerank"
    GENERATION = "generation"
    CUSTOM = "custom"


class TraceStatus(str, Enum):
    """Terminal status of a trace as seen by the client."""

    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
