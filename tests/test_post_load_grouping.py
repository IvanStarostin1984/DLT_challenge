from pathlib import Path

from src.gh_leaderboard import pipeline


def test_post_load_grouping(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "multi_day_commits.json"
    rows = pipeline.run(offline=True, fixture_path=fixture, pipelines_dir=tmp_path)
    assert rows == [
        {"author_identity": "alice", "commit_day": "2024-01-01", "commit_count": 1},
        {"author_identity": "alice", "commit_day": "2024-01-02", "commit_count": 2},
    ]
