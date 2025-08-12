"""Live pipeline test intentionally skipped to avoid network calls."""

import pytest


pytestmark = pytest.mark.skip("requires live GitHub API")


def test_pipeline_live() -> None:  # pragma: no cover - placeholder
    """Placeholder for manual live testing."""
    pass
