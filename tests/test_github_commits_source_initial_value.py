from typing import Any, Dict

import pytest

from src.gh_leaderboard import pipeline
from src.gh_leaderboard.pipeline import github_commits_source


class StubRESTClient:
    last_instance: "StubRESTClient | None" = None

    def __init__(self, base_url: str, headers: Dict[str, Any]) -> None:
        self.base_url = base_url
        self.headers = headers
        self.params: Dict[str, Any] = {}
        StubRESTClient.last_instance = self

    def paginate(self, path: str, params: Dict[str, Any], paginator: Any):
        self.params = params
        yield []


def test_cursor_initial_value_and_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    original_incremental = pipeline.dlt.sources.incremental
    IncrementalCls = original_incremental("cursor").__class__

    class FakeIncremental(IncrementalCls):
        @property
        def last_value(self) -> None:  # type: ignore[override]
            return None

    def fake_incremental(*args: Any, **kwargs: Any) -> FakeIncremental:
        inc = FakeIncremental(*args, **kwargs)
        inc.initial_value = "2024-01-01T00:00:00Z"
        return inc

    monkeypatch.setattr(pipeline.dlt.sources, "incremental", fake_incremental)
    monkeypatch.setattr(pipeline, "RESTClient", StubRESTClient)

    source = github_commits_source()
    commits = source.resources["commits_raw"]
    list(commits())
    rest = StubRESTClient.last_instance
    assert rest is not None
    assert rest.params["since"] == "2023-12-31T23:59:00Z"
    assert "Authorization" not in rest.headers
