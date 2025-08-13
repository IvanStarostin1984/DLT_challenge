from src.gh_leaderboard.pipeline import flatten_commit


def test_flatten_commit_invalid_timestamp() -> None:
    commit = {
        "sha": "bad-timestamp",
        "author": {"login": "alice"},
        "commit": {
            "author": {"name": "Alice", "email": "alice@example.com"},
            "committer": {"date": "not-a-date"},
            "message": "Bad timestamp",
        },
    }
    assert flatten_commit(commit) is None
