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
        self.path = path
        self.params = params
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


def test_authorization_header(
    monkeypatch: pytest.MonkeyPatch, rest_client: type[StubRESTClient]
) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "t0k3n")
    github_commits_source()
    assert rest_client.last_instance.headers["Authorization"] == "Bearer t0k3n"


def test_sha_and_until_params(rest_client: type[StubRESTClient]) -> None:
    source = github_commits_source(branch="main", until="2024-01-01")
    commits = source.resources["commits_raw"]
    list(commits())
    params = rest_client.last_instance.params
    assert params["sha"] == "main"
    assert params["until"] == "2024-01-01"


def test_incremental_adds_since(rest_client: type[StubRESTClient]) -> None:
    source = github_commits_source(since="2024-01-01")
    commits = source.resources["commits_raw"]
    list(commits())
    assert rest_client.last_instance.params["since"] == "2024-01-01"


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
