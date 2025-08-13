from pathlib import Path
import json

from src.gh_leaderboard import pipeline


def test_offline_default_fixture(tmp_path: Path) -> None:
    rows = pipeline.run(offline=True, pipelines_dir=tmp_path)
    assert rows == [
        {
            "author_identity": "sample",
            "commit_day": "2024-01-01",
            "commit_count": 1,
        }
    ]


def test_missing_commit_dates(tmp_path: Path) -> None:
    fixture = [{"sha": "1", "commit": {"author": {"name": "A"}}}]
    path = tmp_path / "missing_dates.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    rows = pipeline.run(offline=True, fixture_path=path, pipelines_dir=tmp_path)
    assert rows == []


def test_mixed_commit_dates(tmp_path: Path) -> None:
    fixture = [
        {
            "sha": "1",
            "author": {"login": "alice"},
            "commit": {
                "author": {
                    "name": "Alice",
                    "date": "2024-01-01T00:00:00Z",
                }
            },
        },
        {
            "sha": "2",
            "author": {"login": "bob"},
            "commit": {"author": {"name": "Bob"}},
        },
    ]
    path = tmp_path / "mixed_dates.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    rows = pipeline.run(offline=True, fixture_path=path, pipelines_dir=tmp_path)
    assert rows == [
        {
            "author_identity": "alice",
            "commit_day": "2024-01-01",
            "commit_count": 1,
        }
    ]


def test_no_commits(tmp_path: Path) -> None:
    path = tmp_path / "empty.json"
    path.write_text("[]", encoding="utf-8")
    rows = pipeline.run(offline=True, fixture_path=path, pipelines_dir=tmp_path)
    assert rows == []
