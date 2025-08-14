"""Pipeline tests including rate-limit retries."""

import os
from pathlib import Path
from typing import Iterator
from unittest.mock import Mock

import duckdb
import pytest
from requests import Response
from dlt.pipeline.exceptions import PipelineStepFailed

from src.gh_leaderboard import pipeline


@pytest.mark.live
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


def test_retry_on_rate_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Retry when the API responds with a rate limit error."""

    commit = {
        "sha": "1",
        "commit": {
            "author": {
                "date": "2023-09-01T00:00:00Z",
                "email": "a@example.com",
                "name": "A",
            },
            "committer": {"date": "2023-09-01T00:00:00Z"},
        },
    }

    resp = Response()
    resp.status_code = 429
    client = Mock()

    def side_effect(*args: object, **kwargs: object) -> Iterator[list[dict]]:
        if not side_effect.called:
            side_effect.called = True
            raise pipeline.RESTClientResponseError(response=resp)
        yield [commit]

    side_effect.called = False
    client.paginate.side_effect = side_effect
    monkeypatch.setattr(pipeline, "RESTClient", lambda *a, **k: client)

    rows = pipeline.run(pipelines_dir=tmp_path)
    assert rows == [
        {
            "author_identity": "a",
            "commit_day": "2023-09-01",
            "commit_count": 1,
        }
    ]
    assert client.paginate.call_count == 2


def test_rate_limit_exhausts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Raise `RuntimeError` after retry attempts are exhausted."""

    resp = Response()
    resp.status_code = 403
    client = Mock()
    client.paginate.side_effect = [
        pipeline.RESTClientResponseError(response=resp),
        pipeline.RESTClientResponseError(response=resp),
        pipeline.RESTClientResponseError(response=resp),
    ]
    monkeypatch.setattr(pipeline, "RESTClient", lambda *a, **k: client)

    with pytest.raises(PipelineStepFailed) as excinfo:
        pipeline.run(pipelines_dir=tmp_path)
    cause = excinfo.value.__cause__
    assert isinstance(cause, Exception)
    assert "GitHub API returned 403" in str(cause)
    assert client.paginate.call_count == 3
