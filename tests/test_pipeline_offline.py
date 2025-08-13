from pathlib import Path

import dlt

from src.gh_leaderboard import pipeline


def test_e2e_pipeline_offline(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "commits.json"
    rows = pipeline.run(offline=True, fixture_path=fixture, pipelines_dir=tmp_path)
    assert rows == [
        {
            "author_identity": "alice",
            "commit_day": "2024-01-01",
            "commit_count": 2,
        },
        {
            "author_identity": "bob",
            "commit_day": "2024-01-02",
            "commit_count": 1,
        },
    ]
    p = dlt.pipeline(
        "gh_leaderboard",
        destination=dlt.destinations.duckdb(str(tmp_path / "leaderboard.duckdb")),
        dataset_name="github_leaderboard",
        pipelines_dir=str(tmp_path),
    )
    with p.sql_client() as sql:
        result = sql.execute_sql(
            "select author_identity, commit_day, commit_count from "
            "leaderboard_daily order by author_identity, commit_day"
        )
    cols = ["author_identity", "commit_day", "commit_count"]
    assert [dict(zip(cols, r)) for r in result] == rows
