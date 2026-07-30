"""Smoke test — validates the SDK can be imported and reports a version."""

from __future__ import annotations

import raglens


def test_version_present() -> None:
    assert isinstance(raglens.__version__, str)
    assert raglens.__version__.count(".") >= 2
