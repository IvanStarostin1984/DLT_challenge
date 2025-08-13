"""Live end-to-end pipeline test."""

import os
from pathlib import Path

import duckdb
import pytest

from src.gh_leaderboard import pipeline

pytestmark = pytest.mark.live


def test_pipeline_live(tmp_path: Path) -> None:
    """Fetch real commits and build a leaderboard."""
    if not os.environ.get("GITHUB_TOKEN"):
        pytest.skip("GITHUB_TOKEN not set")
    rows = pipeline.run(
        repo="pallets/flask",
        since="2023-09-01T00:00:00Z",
        until="2023-09-02T00:00:00Z",
        pipelines_dir=tmp_path,
    )
    assert rows
    assert all(r["commit_count"] >= 1 for r in rows)
    with duckdb.connect(str(tmp_path / "leaderboard.duckdb")) as con:
        assert con.execute("select count(*) from leaderboard_daily").fetchone()[0] >= 1
