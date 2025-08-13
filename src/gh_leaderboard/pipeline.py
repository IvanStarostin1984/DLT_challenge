"""GitHub commit leaderboard pipeline using dlt."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator

logger = logging.getLogger(__name__)


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

    if login and login.strip():
        return login.strip().lower()
    if email:
        local = email.split("@")[0].split("+")[0]
        return local.lower()
    if name and name.strip():
        return name.strip().lower()
    return "unknown"


def flatten_commit(commit: Any) -> Optional[Dict[str, Any]]:
    """Map commit JSON to a skinny row for aggregation."""

    if not isinstance(commit, dict):
        return None
    commit_block = commit.get("commit")
    if not isinstance(commit_block, dict):
        return None
    login = (commit.get("author") or {}).get("login")
    author = commit_block.get("author") or {}
    email = author.get("email")
    name = author.get("name")
    committer = commit_block.get("committer")
    date = committer.get("date") if isinstance(committer, dict) else None
    if not date:
        date = author.get("date")
    if not date:
        logger.info("commit missing timestamp: %s", commit.get("sha"))
        return None
    message = commit_block.get("message")
    message_short = (
        message.splitlines()[0] if isinstance(message, str) and message else None
    )
    return {
        "sha": commit.get("sha"),
        "author_identity": normalize_author(login, email, name),
        "author_login": login,
        "author_email": email,
        "author_name": name,
        "message_short": message_short,
        "commit_timestamp": date,
        "commit_day": date[:10],
    }


@dlt.source
def github_commits_source(
    repo: str = "octocat/Hello-World",
    branch: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
) -> Any:  # pragma: no cover - network source not tested offline
    """GitHub commits source with incremental pagination."""

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params: Dict[str, Any] = {"per_page": 100}
    if branch:
        params["sha"] = branch
    if until:
        params["until"] = until

    client = RESTClient(
        base_url=f"https://api.github.com/repos/{repo}",
        headers=headers,
    )

    @dlt.resource(
        name="commits_raw",
        primary_key="sha",
        write_disposition="append",
    )
    def commits_raw(
        cursor=dlt.sources.incremental("commit.committer.date", initial_value=since),
    ):
        page_params = params.copy()
        if cursor.last_value:
            page_params["since"] = cursor.last_value
        elif cursor.initial_value:
            page_params["since"] = cursor.initial_value
        for page in client.paginate(
            "/commits", params=page_params, paginator=HeaderLinkPaginator()
        ):
            yield from page

    @dlt.transformer(
        data_from=commits_raw,
        name="commits_flat",
        primary_key="sha",
        write_disposition="append",
    )
    def commits_flat(commit: Dict[str, Any]):
        row = flatten_commit(commit)
        if row:
            yield row

    return commits_raw, commits_flat


def run(
    offline: bool = False,
    fixture_path: Optional[str | Path] = None,
    repo: str = "octocat/Hello-World",
    branch: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    pipelines_dir: Optional[str | Path] = None,
) -> List[Dict[str, Any]]:
    """Run the dlt pipeline and return the leaderboard rows."""

    db_path = (
        Path(pipelines_dir) / "leaderboard.duckdb"
        if pipelines_dir
        else Path.cwd() / "leaderboard.duckdb"
    )
    pipeline = dlt.pipeline(
        pipeline_name="gh_leaderboard",
        destination=dlt.destinations.duckdb(str(db_path)),
        dataset_name="github_leaderboard",
        pipelines_dir=str(pipelines_dir) if pipelines_dir else None,
    )

    if offline:
        default_fixture = (
            Path(__file__).resolve().parents[2] / "fixtures" / "commits_sample.json"
        )
        path = Path(fixture_path or default_fixture)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        commits: List[Dict[str, Any]] = (
            [c for c in data if isinstance(c, dict)] if isinstance(data, list) else []
        )
        flat_rows: List[Dict[str, Any]] = []
        for c in commits:
            row = flatten_commit(c)
            if row:
                flat_rows.append(row)
        if not flat_rows:
            return []
        pipeline.run(commits, table_name="commits_raw")
        pipeline.run(flat_rows, table_name="commits_flat")
    else:
        source = github_commits_source(  # pragma: no cover - network call
            repo=repo, branch=branch, since=since, until=until
        )
        pipeline.run(source)  # pragma: no cover - network call

    sql_path = Path(__file__).with_name("post_load.sql")
    with pipeline.sql_client() as sql:
        sql.execute_sql(sql_path.read_text())
        rows = sql.execute_sql(
            "select author_identity, commit_day, commit_count from "
            "leaderboard_daily order by author_identity, commit_day"
        )
    return [
        dict(zip(["author_identity", "commit_day", "commit_count"], r)) for r in rows
    ]


if __name__ == "__main__":
    import argparse

    from .config import load_config

    cfg = load_config()
    parser = argparse.ArgumentParser("GitHub commit leaderboard")
    parser.add_argument("--repo", default=cfg.repo)
    parser.add_argument("--branch", default=cfg.branch)
    parser.add_argument("--since", default=cfg.since)
    parser.add_argument("--until", default=cfg.until)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                offline=args.offline,
                repo=args.repo,
                branch=args.branch,
                since=args.since,
                until=args.until,
            ),
            indent=2,
        )
    )
