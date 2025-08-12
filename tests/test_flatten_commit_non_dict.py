import logging
import pytest

from src.gh_leaderboard.pipeline import flatten_commit


def test_flatten_commit_non_dict_inputs() -> None:
    assert flatten_commit(None) is None
    assert flatten_commit("x") is None


def test_flatten_commit_non_dict_commit_block() -> None:
    assert flatten_commit({"commit": "nope"}) is None


def test_flatten_commit_missing_timestamp_logs(
    caplog: pytest.LogCaptureFixture,
) -> None:
    commit = {"sha": "s", "commit": {"author": {}, "committer": {}}}
    with caplog.at_level(logging.INFO):
        assert flatten_commit(commit) is None
    assert "missing timestamp" in caplog.text
