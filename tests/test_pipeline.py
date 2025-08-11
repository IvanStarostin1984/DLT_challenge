import pytest

from src.gh_leaderboard.pipeline import run


def test_run_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        run()
