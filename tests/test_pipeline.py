from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from gh_leaderboard.pipeline import run


def test_run_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        run()
