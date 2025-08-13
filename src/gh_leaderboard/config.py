"""Configuration helpers for the GitHub leaderboard pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import tomllib


@dataclass
class Settings:
    """Runtime settings for the pipeline."""

    repo: str
    branch: Optional[str] = None
    since: Optional[str] = None
    until: Optional[str] = None
    token: Optional[str] = None


def _read_toml(path: Path) -> dict[str, object]:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


def _parse_iso(value: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_config(path: str | Path = Path(".dlt/config.toml")) -> Settings:
    """Return settings from config file and environment variables.

    Environment variables override values from ``path``. Missing files or
    malformed TOML result in empty defaults.
    """

    path = Path(path)
    data: dict[str, object] = _read_toml(path) if path.is_file() else {}
    defaults = data.get("gh", {}) if isinstance(data, dict) else {}

    repo = os.environ.get("GH_REPO", defaults.get("repo", "octocat/Hello-World"))
    branch = os.environ.get("GH_BRANCH", defaults.get("branch"))
    since = os.environ.get("GH_SINCE_ISO", defaults.get("since"))
    until = os.environ.get("GH_UNTIL_ISO", defaults.get("until"))
    window_days = defaults.get("window_days")

    try:
        days = int(window_days) if window_days is not None else None
    except (TypeError, ValueError):
        days = None

    if days:
        if since and not until:
            start = _parse_iso(since)
            if start:
                until = _iso(start + timedelta(days=days))
        elif until and not since:
            end = _parse_iso(until)
            if end:
                since = _iso(end - timedelta(days=days))
        elif not since and not until:
            end = datetime.utcnow()
            until = _iso(end)
            since = _iso(end - timedelta(days=days))

    token: Optional[str] = None
    secrets_path = path.with_name("secrets.toml")
    if secrets_path.is_file():
        secrets_data = _read_toml(secrets_path)
        if isinstance(secrets_data, dict):
            github = secrets_data.get("github", {})
            if isinstance(github, dict):
                token = github.get("token")
    if token is None:
        token = os.environ.get("GITHUB_TOKEN")

    return Settings(repo=repo, branch=branch, since=since, until=until, token=token)
