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
    data = json.loads(result.stdout)
    assert (
        data
        and {
            "author_identity",
            "commit_day",
            "commit_count",
        }
        <= data[0].keys()
    )
