import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_offline_runs(tmp_path: Path) -> None:
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1])}
    result = subprocess.run(
        [sys.executable, "-m", "src.gh_leaderboard.pipeline", "--offline"],
        check=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=env,
    )
    assert json.loads(result.stdout) == [
        {
            "author_identity": "sample",
            "commit_day": "2024-01-01",
            "commit_count": 1,
        }
    ]
