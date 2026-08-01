"""Dataset schemas — eval datasets are lists of Q&A items with expected answers."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EvalItem(BaseModel):
    """One labeled Q&A pair used in eval / experiments."""

    id: str = Field(..., description="Stable item identifier within the dataset.")
    query: str = Field(..., description="Input query.")
    expected_answer: str | None = Field(
        default=None,
        description="Reference answer. Used by answer_relevancy / faithfulness metrics.",
    )
    expected_chunk_ids: list[str] = Field(
        default_factory=list,
        description="IDs of chunks that *should* be retrieved. Used by context_recall.",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Optional labels: category, difficulty, source.",
    )


class DatasetCreate(BaseModel):
    """Body for POST /v1/datasets."""

    name: str = Field(
        ..., description="Dataset display name.", min_length=1, max_length=255
    )
    items: list[EvalItem] = Field(
        default_factory=list,
        description="Initial items. Can be appended to later via PATCH.",
    )


class DatasetResponse(BaseModel):
    """Dataset GET response."""

    id: uuid.UUID = Field(..., description="Dataset id.")
    project_id: uuid.UUID = Field(..., description="Owning project.")
    name: str = Field(..., description="Dataset name.")
    items: list[EvalItem] = Field(..., description="All items in this dataset.")
    created_at: datetime = Field(..., description="UTC creation timestamp.")
    updated_at: datetime = Field(..., description="UTC last-update timestamp.")

    model_config = ConfigDict(from_attributes=True)
