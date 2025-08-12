from pathlib import Path

from src.gh_leaderboard import pipeline


def test_non_list_fixture(tmp_path: Path) -> None:
    path = tmp_path / "dict.json"
    path.write_text("{}", encoding="utf-8")
    rows = pipeline.run(offline=True, fixture_path=path, pipelines_dir=tmp_path)
    assert rows == []
    assert not (tmp_path / "leaderboard.duckdb").exists()
