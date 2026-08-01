"""Smoke tests for Pydantic schemas.

Goal: catch dumb import / field errors before any HTTP endpoint uses them.
Not exhaustive — that's what W3's ingest tests will do end-to-end.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from app.schemas import (
    Attribution,
    AttributionSource,
    Chunk,
    DatasetCreate,
    DatasetResponse,
    Event,
    EvalItem,
    EventKind,
    ExperimentConfig,
    ExperimentCreate,
    ExperimentResult,
    GenerationEvent,
    ProjectCreate,
    ProjectResponse,
    RetrievalEvent,
    Trace,
    TraceCreate,
    TraceIngestBatch,
    TraceStatus,
)


NOW = datetime.now(timezone.utc)
TRACE_ID = uuid.uuid4()
PROJECT_ID = uuid.uuid4()


def _make_trace(status: TraceStatus = TraceStatus.SUCCESS) -> Trace:
    return Trace(
        id=TRACE_ID,
        project_id=PROJECT_ID,
        query="what is RAG?",
        answer="Retrieval-Augmented Generation.",
        start_time=NOW,
        end_time=NOW,
        duration_ms=42.0,
        status=status,
        cost_usd=0.0001,
    )


def _make_event(kind: EventKind = EventKind.RETRIEVAL) -> Event:
    return Event(
        trace_id=TRACE_ID,
        kind=kind,
        name=f"{kind.value}.step",
        start_time=NOW,
        end_time=NOW,
        duration_ms=1.5,
    )


# ---------------------------------------------------------------------------
# Trace / event
# ---------------------------------------------------------------------------
class TestTraceSchemas:
    def test_trace_roundtrip(self) -> None:
        t = _make_trace()
        assert t.status == TraceStatus.SUCCESS
        assert t.model_dump()["status"] == "success"

    def test_event_forbids_extra_top_level_fields(self) -> None:
        with pytest.raises(ValueError):
            Event(
                trace_id=TRACE_ID,
                kind=EventKind.CUSTOM,
                name="x",
                start_time=NOW,
                end_time=NOW,
                duration_ms=0,
                bogus_field="nope",  # type: ignore[call-arg]
            )

    def test_retrieval_event_kind_locked(self) -> None:
        evt = RetrievalEvent(
            trace_id=TRACE_ID, name="r", start_time=NOW, end_time=NOW, duration_ms=1
        )
        assert evt.kind == EventKind.RETRIEVAL

    def test_generation_event_carries_data(self) -> None:
        evt = GenerationEvent(
            trace_id=TRACE_ID,
            name="claude",
            start_time=NOW,
            end_time=NOW,
            duration_ms=800,
            data={"model": "claude-sonnet-4", "tokens": {"input": 300, "output": 120}},
        )
        assert evt.data["tokens"]["output"] == 120

    def test_chunk_extra_metadata_allowed(self) -> None:
        c = Chunk(id="c1", content="hi", score=0.9, rank=1, extra_field="allowed")  # type: ignore[call-arg]
        assert c.metadata == {}

    def test_ingest_batch_bounds(self) -> None:
        one = TraceCreate(trace=_make_trace(), events=[_make_event()])
        TraceIngestBatch(items=[one])
        with pytest.raises(ValueError):
            TraceIngestBatch(items=[])  # min_length=1

    def test_duration_non_negative(self) -> None:
        with pytest.raises(ValueError):
            Event(
                trace_id=TRACE_ID,
                kind=EventKind.CUSTOM,
                name="x",
                start_time=NOW,
                end_time=NOW,
                duration_ms=-1,
            )


# ---------------------------------------------------------------------------
# Project / Dataset / Attribution / Experiment
# ---------------------------------------------------------------------------
class TestOtherSchemas:
    def test_project_create_min(self) -> None:
        p = ProjectCreate(name="demo")
        assert p.name == "demo"

    def test_project_response_from_attributes(self) -> None:
        # from_attributes lets us build from ORM-like objects
        class FakeModel:
            id = PROJECT_ID
            name = "demo"
            api_key = "rl_xxx"
            created_at = NOW
            updated_at = NOW

        r = ProjectResponse.model_validate(FakeModel())
        assert r.api_key == "rl_xxx"

    def test_dataset_with_items(self) -> None:
        d = DatasetCreate(
            name="test",
            items=[
                EvalItem(id="q1", query="q?", expected_answer="a", expected_chunk_ids=["c1"])
            ],
        )
        assert d.items[0].expected_chunk_ids == ["c1"]

    def test_dataset_response_from_orm_like(self) -> None:
        DatasetResponse(
            id=uuid.uuid4(),
            project_id=PROJECT_ID,
            name="x",
            items=[],
            created_at=NOW,
            updated_at=NOW,
        )

    def test_attribution_source_bounds(self) -> None:
        with pytest.raises(ValueError):
            AttributionSource(chunk_id="c1", score=1.5)  # >1

    def test_attribution_forbids_extra(self) -> None:
        Attribution(
            sentence_index=0,
            sentence_text="s",
            sources=[AttributionSource(chunk_id="c1", score=0.5)],
            method="embedding",
        )
        with pytest.raises(ValueError):
            Attribution(
                sentence_index=0,
                sentence_text="s",
                sources=[],
                method="embedding",
                bogus=1,  # type: ignore[call-arg]
            )

    def test_experiment_config_and_create(self) -> None:
        ExperimentCreate(
            name="chunk_size vs cost",
            dataset_id=uuid.uuid4(),
            variant_a=ExperimentConfig(label="A", params={"chunk_size": 512}),
            variant_b=ExperimentConfig(label="B", params={"chunk_size": 1024}),
        )

    def test_experiment_result_optional_results(self) -> None:
        r = ExperimentResult(
            id=uuid.uuid4(),
            project_id=PROJECT_ID,
            name="x",
            dataset_id=uuid.uuid4(),
            variant_a=ExperimentConfig(label="A"),
            variant_b=ExperimentConfig(label="B"),
            results=None,
            created_at=NOW,
            updated_at=NOW,
        )
        assert r.results is None
