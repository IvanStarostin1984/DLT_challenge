from pathlib import Path

from src.gh_leaderboard import pipeline


def test_nonexistent_fixture(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    rows = pipeline.run(offline=True, fixture_path=missing, pipelines_dir=tmp_path)
    assert rows == []


def test_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("not json", encoding="utf-8")
    rows = pipeline.run(offline=True, fixture_path=path, pipelines_dir=tmp_path)
    assert rows == []
