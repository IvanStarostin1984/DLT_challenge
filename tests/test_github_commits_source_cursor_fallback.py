from typing import Any

import pytest
from jsonpath_ng.ext import parse

from src.gh_leaderboard import pipeline
from src.gh_leaderboard.pipeline import github_commits_source


def test_cursor_falls_back_to_author_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path: str | None = None

    original_incremental = pipeline.dlt.sources.incremental

    def fake_incremental(p: str, *args: Any, **kwargs: Any) -> Any:
        nonlocal path
        path = p
        return original_incremental(p, *args, **kwargs)

    monkeypatch.setattr(pipeline.dlt.sources, "incremental", fake_incremental)
    github_commits_source()
    assert path == "commit['committer','author'].date"

    expr = parse(path)
    commit = {"commit": {"author": {"date": "2024-01-01T00:00:00Z"}}}
    assert [m.value for m in expr.find(commit)] == ["2024-01-01T00:00:00Z"]

    commit_with_committer = {
        "commit": {
            "committer": {"date": "2024-01-02T00:00:00Z"},
            "author": {"date": "2024-01-01T00:00:00Z"},
        }
    }
    assert [m.value for m in expr.find(commit_with_committer)][0] == (
        "2024-01-02T00:00:00Z"
    )
