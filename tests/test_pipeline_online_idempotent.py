from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import dlt
import pytest

from src.gh_leaderboard import pipeline



def test_pipeline_online_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = Path(__file__).parent / "fixtures" / "commits.json"
    commits = json.loads(fixture.read_text(encoding="utf-8"))

    class StubRESTClient:
        def __init__(self, base_url: str, headers: Dict[str, Any]) -> None:
            self.base_url = base_url
            self.headers = headers

        def paginate(
            self, path: str, params: Dict[str, Any], paginator: Any
        ) -> Any:
            yield commits

    monkeypatch.setattr(pipeline, "RESTClient", StubRESTClient)

    pipeline.run(offline=False, pipelines_dir=tmp_path)

    p = dlt.pipeline(
        "gh_leaderboard",
        destination=dlt.destinations.duckdb(str(tmp_path / "leaderboard.duckdb")),
        dataset_name="github_leaderboard",
        pipelines_dir=str(tmp_path),
    )

    with p.sql_client() as sql:
        before = sql.execute_sql("select count(*) from leaderboard_daily")[0][0]

    pipeline.run(offline=False, pipelines_dir=tmp_path)

    with p.sql_client() as sql:
        after = sql.execute_sql("select count(*) from leaderboard_daily")[0][0]
        total, distinct_sha = sql.execute_sql(
            """
            select count(*) as total, count(distinct cf.sha) as distinct_sha
            from leaderboard_daily ld
            join commits_flat cf
            on ld.author_identity = cf.author_identity
            and ld.commit_day = cf.commit_day
            """
        )[0]

    assert before == after
    assert total == distinct_sha
