import pytest

from src.gh_leaderboard.pipeline import flatten_commit


@pytest.fixture
def normal_commit() -> dict:
    return {
        "sha": "1",
        "author": {"login": "alice"},
        "commit": {
            "author": {
                "name": "Alice",
                "email": "alice@example.com",
                "date": "2024-01-01T10:00:00Z",
            },
            "committer": {"date": "2024-01-01T10:00:00Z"},
            "message": "Fix bug\n\nMore details",
        },
    }


@pytest.fixture
def commit_missing_date() -> dict:
    return {
        "sha": "no-date",
        "author": {"login": "alice"},
        "commit": {
            "author": {"name": "Alice", "email": "alice@example.com"},
            "committer": {},
            "message": "No date",
        },
    }


@pytest.fixture
def commit_missing_committer_date() -> dict:
    return {
        "sha": "no-committer-date",
        "author": {"login": "alice"},
        "commit": {
            "author": {
                "name": "Alice",
                "email": "alice@example.com",
                "date": "2024-01-03T10:00:00Z",
            },
            "committer": {},
            "message": "Commit message",
        },
    }


@pytest.fixture
def commit_missing_login() -> dict:
    return {
        "sha": "no-login",
        "author": None,
        "commit": {
            "author": {
                "name": "Bob",
                "email": "bob@example.com",
                "date": "2024-01-02T10:00:00Z",
            },
            "committer": {"date": "2024-01-02T10:00:00Z"},
            "message": "Login missing",
        },
    }


@pytest.fixture
def commit_missing_commit_key() -> dict:
    return {"sha": "no-commit", "author": {"login": "alice"}}


def test_flatten_commit_normal(normal_commit: dict) -> None:
    assert flatten_commit(normal_commit) == {
        "sha": "1",
        "author_identity": "alice",
        "author_login": "alice",
        "author_email": "alice@example.com",
        "author_name": "Alice",
        "message_short": "Fix bug",
        "commit_timestamp": "2024-01-01T10:00:00+00:00",
        "commit_day": "2024-01-01",
    }


def test_flatten_commit_missing_date(commit_missing_date: dict) -> None:
    assert flatten_commit(commit_missing_date) is None


def test_flatten_commit_missing_committer_date(
    commit_missing_committer_date: dict,
) -> None:
    assert flatten_commit(commit_missing_committer_date) == {
        "sha": "no-committer-date",
        "author_identity": "alice",
        "author_login": "alice",
        "author_email": "alice@example.com",
        "author_name": "Alice",
        "message_short": "Commit message",
        "commit_timestamp": "2024-01-03T10:00:00+00:00",
        "commit_day": "2024-01-03",
    }


def test_flatten_commit_missing_login(commit_missing_login: dict) -> None:
    assert flatten_commit(commit_missing_login) == {
        "sha": "no-login",
        "author_identity": "bob",
        "author_login": None,
        "author_email": "bob@example.com",
        "author_name": "Bob",
        "message_short": "Login missing",
        "commit_timestamp": "2024-01-02T10:00:00+00:00",
        "commit_day": "2024-01-02",
    }


def test_flatten_commit_missing_commit_key(
    commit_missing_commit_key: dict,
) -> None:
    assert flatten_commit(commit_missing_commit_key) is None


def test_flatten_commit_non_utc_offset() -> None:
    commit = {
        "sha": "offset",
        "author": {"login": "alice"},
        "commit": {
            "author": {
                "name": "Alice",
                "email": "alice@example.com",
                "date": "2024-01-05T02:30:00+05:00",
            },
            "committer": {"date": "2024-01-05T02:30:00+05:00"},
            "message": "Timezone test",
        },
    }
    assert flatten_commit(commit) == {
        "sha": "offset",
        "author_identity": "alice",
        "author_login": "alice",
        "author_email": "alice@example.com",
        "author_name": "Alice",
        "message_short": "Timezone test",
        "commit_timestamp": "2024-01-04T21:30:00+00:00",
        "commit_day": "2024-01-04",
    }
