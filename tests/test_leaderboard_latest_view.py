from pathlib import Path

import duckdb

from src.gh_leaderboard import pipeline


def test_leaderboard_latest_view(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "three_day_commits.json"
    pipeline.run(offline=True, fixture_path=fixture, pipelines_dir=tmp_path)

    conn = duckdb.connect(tmp_path / "leaderboard.duckdb")
    views = conn.execute(
        "select lower(table_name) from information_schema.views"
        " where table_schema = 'github_leaderboard'"
        " and table_name = 'leaderboard_latest'"
    ).fetchall()
    assert views == [("leaderboard_latest",)]

    count = conn.execute(
        "select count(*) from github_leaderboard.leaderboard_latest"
    ).fetchone()[0]
    assert count == 2

    rows = conn.execute(
        "select commit_day from github_leaderboard.leaderboard_latest"
        " order by commit_day"
    ).fetchall()
    assert rows == [("2024-01-02",), ("2024-01-03",)]
