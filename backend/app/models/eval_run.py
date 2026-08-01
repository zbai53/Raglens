"""EvalRun model — one execution of an evaluation over a dataset.

Named `eval_run.py` (not `eval.py`) to avoid shadowing Python's `eval` builtin
in IDE completion.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, new_uuid

if TYPE_CHECKING:
    from app.models.dataset import Dataset
    from app.models.project import Project


class EvalStatus(str, enum.Enum):
    """Lifecycle of an eval run."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EvalRun(Base):
    __tablename__ = "eval_runs"

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

    # Free-form eval config: {"judge_model": "claude-...", "metrics": [...], ...}
    config: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    status: Mapped[EvalStatus] = mapped_column(
        SAEnum(EvalStatus, name="eval_status", native_enum=True),
        nullable=False,
        default=EvalStatus.PENDING,
        index=True,
    )

    # Aggregated results, e.g. {"faithfulness": 0.82, "context_precision": 0.71, ...}
    metrics: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # -------- relationships --------
    project: Mapped["Project"] = relationship(back_populates="eval_runs")
    dataset: Mapped["Dataset"] = relationship(back_populates="eval_runs")

    def __repr__(self) -> str:
        return f"<EvalRun id={self.id} status={self.status.value}>"
