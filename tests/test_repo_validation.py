import argparse
import json
import subprocess
import sys

import pytest

from src.gh_leaderboard.pipeline import repo_arg


def test_repo_arg_good() -> None:
    assert repo_arg("owner/name") == "owner/name"


def test_repo_arg_bad() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        repo_arg("badformat")


def test_cli_repo_invalid() -> None:
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
    assert "owner/name" in result.stderr


def test_cli_repo_valid() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.gh_leaderboard.pipeline",
            "--repo",
            "foo/bar",
            "--offline",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = json.loads(result.stdout)
    assert isinstance(rows, list)

