"""Project-facing schemas — inbound POST body + outbound API response."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """Body for POST /v1/projects."""

    name: str = Field(
        ..., description="Human-readable project name.", min_length=1, max_length=255
    )


class ProjectResponse(BaseModel):
    """Response body for project endpoints. `api_key` is only returned on create."""

    id: uuid.UUID = Field(..., description="Project identifier (UUID).")
    name: str = Field(..., description="Project name.")
    api_key: str | None = Field(
        default=None,
        description=(
            "Full API key with `rl_` prefix. Only returned on project creation — "
            "subsequent GETs return None (surface via 'reveal key' UI + rotation)."
        ),
    )
    created_at: datetime = Field(..., description="UTC creation timestamp.")
    updated_at: datetime = Field(..., description="UTC last-update timestamp.")

    model_config = ConfigDict(from_attributes=True)
