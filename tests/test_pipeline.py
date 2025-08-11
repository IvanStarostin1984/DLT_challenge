from pathlib import Path

import dlt
import pytest

from src.gh_leaderboard import pipeline


def test_pipeline_live(tmp_path: Path, offline: bool) -> None:
    if offline:
        pytest.skip("offline")
    rows = pipeline.run(
        repo="octocat/Hello-World",
        since="2012-03-06T00:00:00Z",
        until="2012-03-07T00:00:00Z",
        pipelines_dir=tmp_path,
    )
    expected = [
        {
            "author_identity": "octocat",
            "commit_day": "2012-03-06",
            "commit_count": 1,
        }
    ]
    assert rows == expected
    p = dlt.pipeline(
        "gh_leaderboard",
        destination=dlt.destinations.duckdb(str(tmp_path / "leaderboard.duckdb")),
        dataset_name="gh_leaderboard",
        pipelines_dir=str(tmp_path),
    )
    with p.sql_client() as sql:
        result = sql.execute_sql(
            "select author_identity, commit_day, commit_count from "
            "leaderboard_daily order by author_identity, commit_day"
        )
    cols = ["author_identity", "commit_day", "commit_count"]
    assert [dict(zip(cols, r)) for r in result] == expected
