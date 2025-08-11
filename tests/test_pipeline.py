from pathlib import Path

import pytest

from src.gh_leaderboard import pipeline


def test_pipeline_live(tmp_path: Path, offline: bool) -> None:
    if offline:
        pytest.skip("offline")
    state = tmp_path / "state.json"
    rows = pipeline.run(
        repo="octocat/Hello-World",
        since="2012-03-06T00:00:00Z",
        until="2012-03-07T00:00:00Z",
        state_path=state,
    )
    assert rows == [
        {
            "author_identity": "octocat",
            "commit_day": "2012-03-06",
            "commit_count": 1,
        }
    ]
