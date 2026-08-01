"""SQLAlchemy async foundations.

Everything DB-model related builds on this file:

- `engine` / `async_session_factory` — global connection pool + session factory
- `Base` — DeclarativeBase with a strict naming convention so Alembic-generated
  migrations produce deterministic constraint/index names
- `get_session` — FastAPI dependency yielding one session per request
- `TimestampMixin` — reusable created_at / updated_at columns
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from app.config import settings

# ---------------------------------------------------------------------------
# Naming convention — MUST match Alembic's target_metadata for stable diffs.
# Without this, Alembic invents constraint names like `dataset_project_id_fkey`
# on Postgres but different names elsewhere, producing dirty migrations.
# ---------------------------------------------------------------------------
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(AsyncAttrs, DeclarativeBase):
    """Project-wide declarative base. All models inherit from this."""

    metadata = metadata


class TimestampMixin:
    """Adds server-default `created_at` and auto-updated `updated_at`."""

    created_at: Mapped[datetime] = mapped_column(
        default=None,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=None,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def new_uuid() -> uuid.UUID:
    """UUID4 factory. Kept in one place so we can swap to ULID / UUIDv7 later."""
    return uuid.uuid4()


# ---------------------------------------------------------------------------
# Engine + session factory (module-level singletons)
# ---------------------------------------------------------------------------
engine = create_async_engine(
    settings.database_url,
    # 20 conns is the target for W1; adjust based on real backend concurrency later.
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,           # detect stale conns after PG restart
    pool_recycle=1800,            # drop conns older than 30 min
    echo=False,
    future=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,       # keeps returned ORM objects usable after commit
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yield one AsyncSession per request, rollback on error."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
