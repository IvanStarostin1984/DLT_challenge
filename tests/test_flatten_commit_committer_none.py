from src.gh_leaderboard.pipeline import flatten_commit


def test_flatten_commit_committer_none_returns_none() -> None:
    commit = {"sha": "no-committer", "commit": {"committer": None}}
    assert flatten_commit(commit) is None


def test_flatten_commit_missing_author_block_uses_unknown() -> None:
    commit = {
        "sha": "2",
        "commit": {"committer": {"date": "2024-01-04T10:00:00Z"}},
    }
    assert flatten_commit(commit) == {
        "sha": "2",
        "author_identity": "unknown",
        "commit_timestamp": "2024-01-04T10:00:00Z",
        "commit_day": "2024-01-04",
    }
