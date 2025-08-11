from src.gh_leaderboard.pipeline import normalize_author


def test_normalize_author_preference() -> None:
    assert normalize_author("alice", "alice@example.com", "Alice") == "alice"
    assert normalize_author(None, "Bob+spam@Example.com", None) == "bob"
    assert normalize_author(None, None, "  Carol  ") == "carol"
    assert normalize_author(None, None, None) == "unknown"
