from src.gh_leaderboard.pipeline import normalize_author


def test_normalize_author_empty_email() -> None:
    assert normalize_author(None, "", "Alice") == "alice"
    assert normalize_author("   ", "", None) == "unknown"
