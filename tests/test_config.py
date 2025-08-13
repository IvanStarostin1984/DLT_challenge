from datetime import datetime
from pathlib import Path

import src.gh_leaderboard.config as cfg


def _write_config(tmp_path: Path, body: str = "") -> Path:
    cfg_dir = tmp_path / ".dlt"
    cfg_dir.mkdir()
    cfg_file = cfg_dir / "config.toml"
    cfg_file.write_text(f'[gh]\nrepo="r1"\nbranch="b1"\n{body}', encoding="utf-8")
    return cfg_file


class _FixedDatetime(datetime):
    @classmethod
    def utcnow(cls):
        return cls(2024, 1, 15, 0, 0, 0)


def test_window_days_computation(tmp_path: Path, monkeypatch) -> None:
    cfg_file = _write_config(tmp_path, "window_days=7\n")
    monkeypatch.setattr(cfg, "datetime", _FixedDatetime)
    settings = cfg.load_config(cfg_file)
    assert settings.since == "2024-01-08T00:00:00Z"
    assert settings.until == "2024-01-15T00:00:00Z"


def test_env_overrides(tmp_path: Path, monkeypatch) -> None:
    cfg_file = _write_config(tmp_path, "window_days=7\n")
    monkeypatch.setenv("GH_REPO", "r2")
    monkeypatch.setenv("GH_BRANCH", "b2")
    monkeypatch.setenv("GH_SINCE_ISO", "2024-02-01T00:00:00Z")
    monkeypatch.setenv("GH_UNTIL_ISO", "2024-02-15T00:00:00Z")
    settings = cfg.load_config(cfg_file)
    assert settings.repo == "r2"
    assert settings.branch == "b2"
    assert settings.since == "2024-02-01T00:00:00Z"
    assert settings.until == "2024-02-15T00:00:00Z"


def test_token_from_secrets(tmp_path: Path, monkeypatch) -> None:
    cfg_file = _write_config(tmp_path)
    secrets = cfg_file.with_name("secrets.toml")
    secrets.write_text('[github]\ntoken="s3cret"', encoding="utf-8")
    monkeypatch.setenv("GITHUB_TOKEN", "envtok")
    settings = cfg.load_config(cfg_file)
    assert settings.token == "s3cret"


def test_token_from_env(tmp_path: Path, monkeypatch) -> None:
    cfg_file = _write_config(tmp_path)
    monkeypatch.setenv("GITHUB_TOKEN", "envtok")
    settings = cfg.load_config(cfg_file)
    assert settings.token == "envtok"
