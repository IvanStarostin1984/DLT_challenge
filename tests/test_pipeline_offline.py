from pathlib import Path

from src.gh_leaderboard import pipeline


def test_pipeline_offline() -> None:
    fixture = Path(__file__).parent / "fixtures" / "commits.json"
    rows = pipeline.run(offline=True, fixture_path=fixture)
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
