import json
import logging
from pathlib import Path

import pytest

from src.gh_leaderboard import pipeline


def test_run_skips_non_dict_and_logs(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    fixture = tmp_path / "commits.json"
    data = [1, "a", {"sha": "s", "commit": {"author": {}, "committer": {}}}]
    fixture.write_text(json.dumps(data))
    with caplog.at_level(logging.INFO):
        rows = pipeline.run(
            offline=True, fixture_path=str(fixture), pipelines_dir=tmp_path
        )
    assert rows == []
    assert "missing timestamp" in caplog.text
