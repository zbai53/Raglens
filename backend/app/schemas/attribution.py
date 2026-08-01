"""Attribution schemas — answer sentences ↔ source chunks.

Two-level design:
- Level 1 (fast, always-on): sentence embedding × chunk embedding cosine sim.
- Level 2 (slow, opt-in): LLM-as-judge scoring per sentence/chunk pair.

The API shape is the same for both; only `method` tells clients what they got.
"""

from __future__ import annotations

import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AttributionSource(BaseModel):
    """One source chunk backing a specific answer sentence."""

    chunk_id: str = Field(..., description="ID of the chunk that contributed.")
    score: float = Field(
        ...,
        description="Attribution strength in [0, 1]. Method-dependent: cosine or judge score.",
        ge=0.0,
        le=1.0,
    )


class Attribution(BaseModel):
    """Attribution result for one answer sentence."""

    sentence_index: int = Field(
        ..., description="0-based index of the answer sentence.", ge=0
    )
    sentence_text: str = Field(..., description="The sentence itself (for UI hover/highlight).")
    sources: list[AttributionSource] = Field(
        default_factory=list,
        description="Contributing chunks, sorted by score desc. May be empty for hallucinated text.",
    )
    method: Literal["embedding", "llm_judge"] = Field(
        ..., description="Which scoring method produced these sources."
    )

    model_config = ConfigDict(extra="forbid")


class TraceAttribution(BaseModel):
    """Wrapper — full attribution for a single trace's answer."""

    trace_id: uuid.UUID = Field(..., description="Trace this attribution belongs to.")
    attributions: list[Attribution] = Field(
        default_factory=list,
        description="One entry per sentence in the answer, in order.",
    )
