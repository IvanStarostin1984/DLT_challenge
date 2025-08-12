from typing import Any, Dict

import pytest

from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator
from src.gh_leaderboard import pipeline
from src.gh_leaderboard.pipeline import github_commits_source


class StubRESTClient:
    last_instance: "StubRESTClient | None" = None

    def __init__(self, base_url: str, headers: Dict[str, Any]) -> None:
        self.base_url = base_url
        self.headers = headers
        self.params: Dict[str, Any] = {}
        self.paginator: Any | None = None
        StubRESTClient.last_instance = self

    def paginate(self, path: str, params: Dict[str, Any], paginator: Any):
        self.params = params
        self.paginator = paginator
        yield []


def test_cursor_last_value_and_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    original_incremental = pipeline.dlt.sources.incremental

    IncrementalCls = original_incremental("cursor").__class__

    class FakeIncremental(IncrementalCls):
        @property
        def last_value(self) -> str:  # type: ignore[override]
            return "2024-02-02T00:00:00Z"

    def fake_incremental(*args: Any, **kwargs: Any) -> FakeIncremental:
        return FakeIncremental(*args, **kwargs)

    monkeypatch.setattr(pipeline.dlt.sources, "incremental", fake_incremental)
    monkeypatch.setattr(pipeline, "RESTClient", StubRESTClient)

    source = github_commits_source()
    commits = source.resources["commits"]
    list(commits())
    rest = StubRESTClient.last_instance
    assert rest is not None
    assert rest.params["since"] == "2024-02-02T00:00:00Z"
    assert "Authorization" not in rest.headers
    assert isinstance(rest.paginator, HeaderLinkPaginator)
