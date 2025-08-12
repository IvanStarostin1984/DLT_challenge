from src.gh_leaderboard.pipeline import normalize_author


def test_login_is_lowercased() -> None:
    assert normalize_author("ALICE", None, None) == "alice"


def test_whitespace_login_falls_back() -> None:
    assert normalize_author("", "Bob@example.com", None) == "bob"
    assert normalize_author("   ", None, "Carol") == "carol"


def test_blank_name_returns_unknown() -> None:
    assert normalize_author(None, None, "   ") == "unknown"
