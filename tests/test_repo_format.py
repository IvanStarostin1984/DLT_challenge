import subprocess
import sys

import pytest

from src.gh_leaderboard.pipeline import validate_repo


def test_validate_repo_good() -> None:
    assert validate_repo("foo/bar") == "foo/bar"


def test_validate_repo_bad() -> None:
    with pytest.raises(ValueError, match="repo must be in owner/name format"):
        validate_repo("badformat")


def test_cli_invalid_repo() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.gh_leaderboard.pipeline",
            "--repo",
            "badformat",
            "--offline",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "repo must be in owner/name format" in result.stderr
