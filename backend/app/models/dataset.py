"""Dataset model — labeled Q&A pairs used for eval and A/B experiments.

The `items` JSONB column holds a list of `EvalItem` (see schemas/dataset.py):
    { "id": "...", "query": "...", "expected_answer": "...",
      "expected_chunk_ids": ["..."] }
Storing as JSONB (vs a separate items table) keeps eval loading in one query
and matches the natural read pattern: load whole dataset → iterate.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, new_uuid

if TYPE_CHECKING:
    from app.models.eval_run import EvalRun
    from app.models.experiment import Experiment
    from app.models.project import Project


class Dataset(TimestampMixin, Base):
    __tablename__ = "datasets"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    items: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB, nullable=False, default=list
    )

    # -------- relationships --------
    project: Mapped["Project"] = relationship(back_populates="datasets")
    eval_runs: Mapped[list["EvalRun"]] = relationship(
        back_populates="dataset", cascade="all, delete-orphan"
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        back_populates="dataset"
    )

    def __repr__(self) -> str:
        return f"<Dataset id={self.id} name={self.name!r} items={len(self.items)}>"
