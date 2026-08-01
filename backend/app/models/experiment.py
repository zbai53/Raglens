"""Experiment model — an A/B comparison between two RAG configurations.

Both `variant_a` and `variant_b` are opaque JSONB blobs (chunk_size, top_k,
retriever type, prompt template — whatever the user wants to compare).
`results` is populated after the experiment finishes: per-metric deltas,
per-item breakdown, bootstrap CIs.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, new_uuid

if TYPE_CHECKING:
    from app.models.dataset import Dataset
    from app.models.project import Project


class Experiment(TimestampMixin, Base):
    __tablename__ = "experiments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=new_uuid,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    variant_a: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    variant_b: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # {"a": {"faithfulness": 0.82, ...}, "b": {...}, "diffs": {...}, "ci": {...}}
    results: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    # -------- relationships --------
    project: Mapped["Project"] = relationship(back_populates="experiments")
    dataset: Mapped["Dataset"] = relationship(back_populates="experiments")

    def __repr__(self) -> str:
        return f"<Experiment id={self.id} name={self.name!r}>"
