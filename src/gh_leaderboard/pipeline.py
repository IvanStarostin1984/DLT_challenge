"""Offline GitHub leaderboard pipeline."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional


def normalize_author(
    login: Optional[str], email: Optional[str], name: Optional[str]
) -> str:
    """Return a stable author identity.

    Preference order:
    1. GitHub login.
    2. Local part of email (strips "+tag").
    3. Normalised name.
    4. "unknown".
    """

    if login:
        return login.lower()
    if email:
        local = email.split("@")[0].split("+")[0]
        return local.lower()
    if name:
        return name.strip().lower()
    return "unknown"


def run(
    offline: bool = False, fixture_path: Optional[str | Path] = None
) -> List[Dict[str, Any]]:
    """Run the pipeline.

    When ``offline`` is true, commits are read from ``fixture_path`` and
    aggregated into a simple leaderboard.
    """

    if not offline:
        raise NotImplementedError("Live mode not implemented.")

    path = Path(fixture_path or Path(__file__).with_name("commits_fixture.json"))
    with path.open() as f:
        commits = json.load(f)

    counts: Dict[tuple[str, str], int] = defaultdict(int)
    for commit in commits:
        login = (commit.get("author") or {}).get("login")
        author_info = commit.get("commit", {}).get("author") or {}
        email = author_info.get("email")
        name = author_info.get("name")
        date = author_info.get("date") or commit.get("commit", {}).get(
            "committer", {}
        ).get("date")
        if not date:
            continue
        day = date[:10]
        identity = normalize_author(login, email, name)
        counts[(identity, day)] += 1

    leaderboard = [
        {"author_identity": author, "commit_day": day, "commit_count": count}
        for (author, day), count in sorted(counts.items())
    ]
    return leaderboard
