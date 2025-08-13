"""Configuration helpers for the GitHub leaderboard pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
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


def load_config(path: str | Path = Path(".dlt/config.toml")) -> Settings:
    """Return settings from config file and environment variables.

    Environment variables override values from ``path``. Missing files or
    malformed TOML result in empty defaults.
    """

    path = Path(path)
    data: dict[str, object] = {}
    if path.is_file():
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            data = {}
    defaults = data.get("github_leaderboard", {}) if isinstance(data, dict) else {}
    return Settings(
        repo=os.environ.get("GH_REPO", defaults.get("repo", "octocat/Hello-World")),
        branch=os.environ.get("GH_BRANCH", defaults.get("branch")),
        since=os.environ.get("GH_SINCE_ISO", defaults.get("since")),
        until=os.environ.get("GH_UNTIL_ISO", defaults.get("until")),
    )
