"""Project model — a project is the top-level tenant for RagLens.

Each user's RAG app corresponds to one project. All traces, datasets, eval
runs, and experiments are scoped to a project via api_key authentication.
"""

from __future__ import annotations

import secrets
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, new_uuid

if TYPE_CHECKING:
    from app.models.dataset import Dataset
    from app.models.eval_run import EvalRun
    from app.models.experiment import Experiment


API_KEY_PREFIX = "rl_"
API_KEY_ENTROPY_BYTES = 32  # secrets.token_urlsafe(32) → 43-char string


def new_api_key() -> str:
    """Generate `rl_<43 url-safe chars>` — 256 bits of entropy."""
    return f"{API_KEY_PREFIX}{secrets.token_urlsafe(API_KEY_ENTROPY_BYTES)}"


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=new_uuid,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        default=new_api_key,
    )

    # -------- relationships --------
    datasets: Mapped[list["Dataset"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    eval_runs: Mapped[list["EvalRun"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.name!r}>"
