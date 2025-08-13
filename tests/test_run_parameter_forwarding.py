from pathlib import Path
from typing import Any, Dict, List

import dlt
from src.gh_leaderboard import pipeline


def test_run_parameter_forwarding(tmp_path: Path, monkeypatch: Any) -> None:
    repo = "my/repo"
    branch = "main"
    since = "2024-01-01T00:00:00Z"
    until = "2024-01-02T00:00:00Z"
    captured: Dict[str, Any] = {}

    def fake_source(
        *, repo: str, branch: str, since: str, until: str
    ) -> List[Dict[str, Any]]:
        captured["source"] = {
            "repo": repo,
            "branch": branch,
            "since": since,
            "until": until,
        }
        return []

    db_path = tmp_path / "leaderboard.duckdb"

    def fake_pipeline(
        *,
        pipeline_name: str,
        destination: Any,
        dataset_name: str,
        pipelines_dir: str | None
    ) -> Any:
        captured["pipeline"] = {
            "pipeline_name": pipeline_name,
            "dataset_name": dataset_name,
            "pipelines_dir": pipelines_dir,
        }

        class FakePipeline:
            def run(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - stub
                db_path.touch()

            def sql_client(self) -> Any:  # pragma: no cover - stub
                class Client:
                    def __enter__(self_inner) -> "Client":
                        return self_inner

                    def __exit__(self_inner, exc_type, exc, tb) -> None:
                        pass

                    def execute_sql(self_inner, sql: str) -> List[tuple]:
                        if sql.lower().startswith("select"):
                            return [("alice", "2024-01-01", 1)]
                        return []

                return Client()

        return FakePipeline()

    monkeypatch.setattr(pipeline, "github_commits_source", fake_source)
    monkeypatch.setattr(dlt, "pipeline", fake_pipeline)

    rows = pipeline.run(
        offline=False,
        repo=repo,
        branch=branch,
        since=since,
        until=until,
        pipelines_dir=tmp_path,
    )

    assert captured["source"] == {
        "repo": repo,
        "branch": branch,
        "since": since,
        "until": until,
    }
    assert captured["pipeline"] == {
        "pipeline_name": "gh_leaderboard",
        "dataset_name": "gh_leaderboard",
        "pipelines_dir": str(tmp_path),
    }
    assert db_path.exists()
    assert rows == [
        {
            "author_identity": "alice",
            "commit_day": "2024-01-01",
            "commit_count": 1,
        }
    ]
