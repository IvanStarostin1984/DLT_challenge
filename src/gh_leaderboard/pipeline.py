"""GitHub commit leaderboard pipeline."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


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
    offline: bool = False,
    fixture_path: Optional[str | Path] = None,
    repo: str = "octocat/Hello-World",
    branch: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    state_path: Optional[str | Path] = Path(".dlt/state.json"),
) -> List[Dict[str, Any]]:
    """Run the pipeline.

    When ``offline`` is true, commits are read from ``fixture_path`` and
    aggregated into a simple leaderboard.

    In live mode commits are fetched from GitHub. Pagination, incremental
    loading and author normalisation follow ``docs/specs.txt``.
    """

    if offline:
        path = Path(fixture_path or Path(__file__).with_name("commits_fixture.json"))
        with path.open() as f:
            commits = json.load(f)
    else:
        token = os.environ.get("GITHUB_TOKEN")

        # derive since from state when not provided
        if state_path and since is None:
            try:
                state = json.loads(Path(state_path).read_text())
                since = state.get(repo)
            except FileNotFoundError:
                pass

        params = {"per_page": 100}
        if branch:
            params["sha"] = branch
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        url = f"https://api.github.com/repos/{repo}/commits"
        commits: List[Dict[str, Any]] = []
        while url:
            try:
                resp = requests.get(url, params=params, headers=headers, timeout=30)
                resp.raise_for_status()
            except requests.RequestException as exc:  # pragma: no cover - network
                raise RuntimeError("GitHub API request failed") from exc
            data = resp.json()
            if not isinstance(data, list):
                break
            commits.extend(data)
            link = resp.headers.get("Link", "")
            next_url = None
            for part in link.split(","):
                if 'rel="next"' in part:
                    next_url = part[part.find("<") + 1 : part.find(">")]
                    break
            url = next_url
            params = None

    counts: Dict[tuple[str, str], int] = defaultdict(int)
    max_cursor = since
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
        if max_cursor is None or date > max_cursor:
            max_cursor = date
        day = date[:10]
        identity = normalize_author(login, email, name)
        counts[(identity, day)] += 1

    if state_path and max_cursor:
        path = Path(state_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            state = json.loads(path.read_text())
        except FileNotFoundError:
            state = {}
        state[repo] = max_cursor
        path.write_text(json.dumps(state))

    leaderboard = [
        {"author_identity": author, "commit_day": day, "commit_count": count}
        for (author, day), count in sorted(counts.items())
    ]
    return leaderboard
