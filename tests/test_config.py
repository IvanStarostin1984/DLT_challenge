from pathlib import Path

from src.gh_leaderboard.config import load_config


def _write_config(tmp_path: Path) -> Path:
    cfg_dir = tmp_path / ".dlt"
    cfg_dir.mkdir()
    cfg_file = cfg_dir / "config.toml"
    cfg_file.write_text(
        """[github_leaderboard]
repo="r1"
branch="b1"
since="2024-01-01T00:00:00Z"
until="2024-01-15T00:00:00Z"
""",
        encoding="utf-8",
    )
    return cfg_file


def test_load_config_file(tmp_path: Path) -> None:
    cfg_file = _write_config(tmp_path)
    settings = load_config(cfg_file)
    assert settings.repo == "r1"
    assert settings.branch == "b1"
    assert settings.since == "2024-01-01T00:00:00Z"
    assert settings.until == "2024-01-15T00:00:00Z"


def test_env_overrides(tmp_path: Path, monkeypatch) -> None:
    cfg_file = _write_config(tmp_path)
    monkeypatch.setenv("GH_REPO", "r2")
    monkeypatch.setenv("GH_BRANCH", "b2")
    monkeypatch.setenv("GH_SINCE_ISO", "2024-02-01T00:00:00Z")
    monkeypatch.setenv("GH_UNTIL_ISO", "2024-02-15T00:00:00Z")
    settings = load_config(cfg_file)
    assert settings.repo == "r2"
    assert settings.branch == "b2"
    assert settings.since == "2024-02-01T00:00:00Z"
    assert settings.until == "2024-02-15T00:00:00Z"
