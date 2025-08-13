from pathlib import Path
import os

from src.gh_leaderboard import pipeline


def test_run_default_path(tmp_path: Path) -> None:
    prev_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        rows = pipeline.run(offline=True)
    finally:
        os.chdir(prev_cwd)
    assert (tmp_path / "leaderboard.duckdb").exists()
    assert rows == [
        {
            "author_identity": "sample",
            "commit_day": "2024-01-01",
            "commit_count": 1,
        }
    ]
