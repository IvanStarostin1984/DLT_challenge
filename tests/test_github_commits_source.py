from typing import Any, Dict

import pytest
from dlt.sources.helpers.rest_client.client import (
    HTTPError as RESTClientResponseError,
)
from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator
from dlt.extract.exceptions import ResourceExtractionError

from src.gh_leaderboard import pipeline
from src.gh_leaderboard.pipeline import github_commits_source
from src.gh_leaderboard.config import Settings


class StubRESTClient:
    last_instance: "StubRESTClient | None" = None

    def __init__(self, base_url: str, headers: Dict[str, Any]) -> None:
        self.base_url = base_url
        self.headers = headers
        self.params: Dict[str, Any] = {}
        self.paginator: HeaderLinkPaginator | None = None
        StubRESTClient.last_instance = self

    def paginate(
        self,
        path: str,
        params: Dict[str, Any],
        paginator: HeaderLinkPaginator,
    ) -> Any:
        self.path = path
        self.params = params
        self.paginator = paginator
        yield []


class Cursor:
    def __init__(
        self,
        last_value: str | None = None,
        initial_value: str | None = None,
    ) -> None:
        self.last_value = last_value
        self.initial_value = initial_value


@pytest.fixture
def rest_client(monkeypatch: pytest.MonkeyPatch) -> type[StubRESTClient]:
    monkeypatch.setattr(pipeline, "RESTClient", StubRESTClient)
    return StubRESTClient


def test_authorization_header(rest_client: type[StubRESTClient]) -> None:
    cfg = Settings(repo="octocat/Hello-World", token="t0k3n")
    github_commits_source(repo=cfg.repo, token=cfg.token)
    assert rest_client.last_instance.headers["Authorization"] == "Bearer t0k3n"


def test_sha_and_until_params(rest_client: type[StubRESTClient]) -> None:
    source = github_commits_source(branch="main", until="2024-01-01")
    commits = source.resources["commits_raw"]
    list(commits())
    params = rest_client.last_instance.params
    assert params["sha"] == "main"
    assert params["until"] == "2024-01-01"


def test_incremental_adds_since(rest_client: type[StubRESTClient]) -> None:
    source = github_commits_source(since="2024-01-01T00:00:00Z")
    commits = source.resources["commits_raw"]
    list(commits())
    assert rest_client.last_instance.params["since"] == "2023-12-31T23:59:00Z"


def test_client_base_url_and_per_page_default(
    rest_client: type[StubRESTClient],
) -> None:
    source = github_commits_source(repo="owner/repo")
    commits = source.resources["commits_raw"]
    list(commits())
    assert rest_client.last_instance.base_url == (
        "https://api.github.com/repos/owner/repo"
    )
    assert rest_client.last_instance.params["per_page"] == 100


def test_paginator_type(rest_client: type[StubRESTClient]) -> None:
    source = github_commits_source()
    commits = source.resources["commits_raw"]
    list(commits())
    assert isinstance(rest_client.last_instance.paginator, HeaderLinkPaginator)


def test_commits_raw_403_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    class ErrorRESTClient(StubRESTClient):
        def paginate(
            self, path: str, params: Dict[str, Any], paginator: HeaderLinkPaginator
        ) -> Any:
            from requests import Response

            resp = Response()
            resp.status_code = 403
            raise RESTClientResponseError("Forbidden", response=resp)

    monkeypatch.setattr(pipeline, "RESTClient", ErrorRESTClient)
    commits = github_commits_source().resources["commits_raw"]
    with pytest.raises(ResourceExtractionError) as excinfo:
        list(commits())
    assert isinstance(excinfo.value.__cause__, RuntimeError)
    assert "GitHub API returned 403" in str(excinfo.value.__cause__)
