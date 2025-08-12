from pathlib import Path
import os

from src.gh_leaderboard import pipeline


def test_run_default_path(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "commits.json"
    prev_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        rows = pipeline.run(offline=True, fixture_path=fixture)
    finally:
        os.chdir(prev_cwd)
    assert (tmp_path / "leaderboard.duckdb").exists()
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
