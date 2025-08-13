from typing import Any, Dict

import pytest

from src.gh_leaderboard import pipeline
from src.gh_leaderboard.pipeline import github_commits_source


class StubRESTClient:
    def __init__(self, base_url: str, headers: Dict[str, Any]) -> None:
        self.base_url = base_url
        self.headers = headers

    def paginate(self, path: str, params: Dict[str, Any], paginator: Any):
        yield []


def test_commits_flat(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pipeline, "RESTClient", StubRESTClient)
    source = github_commits_source()
    commits_flat = source.resources["commits_flat"]
    commit = {
        "sha": "abc123",
        "author": {"login": "alice"},
        "commit": {
            "author": {
                "name": "Alice",
                "email": "alice@example.com",
            },
            "committer": {"date": "2024-01-01T10:00:00Z"},
            "message": "Message head\nbody",
        },
    }
    assert list(commits_flat._pipe.gen(commit)) == [
        {
            "sha": "abc123",
            "author_identity": "alice",
            "author_login": "alice",
            "author_email": "alice@example.com",
            "author_name": "Alice",
            "message_short": "Message head",
            "commit_timestamp": "2024-01-01T10:00:00+00:00",
            "commit_day": "2024-01-01",
        }
    ]
