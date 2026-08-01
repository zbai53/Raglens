"""Experiment schemas — A/B compare two RAG configurations on a dataset."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ExperimentConfig(BaseModel):
    """One arm of an A/B experiment — an opaque config blob.

    Shape is user-defined: could hold chunk_size, top_k, retriever, prompt
    template, etc. The eval runner reads it and reproduces the pipeline.
    """

    label: str = Field(
        ..., description="Short arm label, e.g. 'chunk_size=512' or 'variant-A'.",
        min_length=1, max_length=64,
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Free-form pipeline configuration parameters for this arm.",
    )


class ExperimentCreate(BaseModel):
    """Body for POST /v1/experiments."""

    name: str = Field(
        ..., description="Human-readable experiment name.", min_length=1, max_length=255
    )
    dataset_id: uuid.UUID = Field(..., description="Dataset to evaluate both arms against.")
    variant_a: ExperimentConfig = Field(..., description="Arm A configuration.")
    variant_b: ExperimentConfig = Field(..., description="Arm B configuration.")


class ExperimentResult(BaseModel):
    """Aggregated result after the experiment finishes."""

    id: uuid.UUID = Field(..., description="Experiment id.")
    project_id: uuid.UUID = Field(..., description="Owning project.")
    name: str = Field(..., description="Experiment name.")
    dataset_id: uuid.UUID = Field(..., description="Dataset used.")
    variant_a: ExperimentConfig = Field(..., description="Arm A config.")
    variant_b: ExperimentConfig = Field(..., description="Arm B config.")
    results: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Aggregated results: {'a': {metric: score}, 'b': {metric: score}, "
            "'diffs': {metric: delta}, 'ci': {metric: [lo, hi]}}. None if not yet run."
        ),
    )
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last-update timestamp.")

    model_config = ConfigDict(from_attributes=True)
