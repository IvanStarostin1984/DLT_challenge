import json
import subprocess
import sys


def test_cli_offline_runs() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "src.gh_leaderboard.pipeline", "--offline"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(result.stdout) == []
