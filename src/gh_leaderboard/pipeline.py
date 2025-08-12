"""GitHub commit leaderboard pipeline using dlt."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator


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
    if name:
        return name.strip().lower()
    return "unknown"


def flatten_commit(commit: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Map commit JSON to a skinny row for aggregation."""

    login = (commit.get("author") or {}).get("login")
    author = commit.get("commit", {}).get("author") or {}
    email = author.get("email")
    name = author.get("name")
    date = commit.get("commit", {}).get("committer", {}).get("date") or author.get(
        "date"
    )
    if not date:
        return None
    return {
        "sha": commit.get("sha"),
        "author_identity": normalize_author(login, email, name),
        "commit_timestamp": date,
        "commit_day": date[:10],
    }


@dlt.source
def github_commits_source(
    repo: str = "octocat/Hello-World",
    branch: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
):
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
        name="commits",
        primary_key="sha",
        write_disposition="append",
    )
    def commits(
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
        data_from=commits,
        name="commits_flat",
        primary_key="sha",
        write_disposition="append",
    )
    def commits_flat(commit: Dict[str, Any]):
        row = flatten_commit(commit)
        if row:
            yield row

    return commits, commits_flat


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
        else Path("leaderboard.duckdb")
    )
    pipeline = dlt.pipeline(
        pipeline_name="gh_leaderboard",
        destination=dlt.destinations.duckdb(str(db_path)),
        dataset_name="gh_leaderboard",
        pipelines_dir=str(pipelines_dir) if pipelines_dir else None,
    )

    if offline:
        path = Path(fixture_path or Path(__file__).with_name("commits_fixture.json"))
        commits: Iterable[Dict[str, Any]] = json.loads(path.read_text())
        pipeline.run(commits, table_name="commits")
        pipeline.run(
            (row for row in (flatten_commit(c) for c in commits) if row),
            table_name="commits_flat",
        )
    else:
        source = github_commits_source(
            repo=repo, branch=branch, since=since, until=until
        )
        pipeline.run(source)

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
