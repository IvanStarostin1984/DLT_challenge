from pathlib import Path

import duckdb

from src.gh_leaderboard import pipeline


def test_non_list_fixture(tmp_path: Path) -> None:
    path = tmp_path / "dict.json"
    path.write_text("{}", encoding="utf-8")
    rows = pipeline.run(offline=True, fixture_path=path, pipelines_dir=tmp_path)
    assert rows == []
    con = duckdb.connect(str(tmp_path / "leaderboard.duckdb"))
    assert (
        con.execute("select count(*) from github_leaderboard.commits_raw").fetchone()[0]
        == 0
    )
    assert (
        con.execute("select count(*) from github_leaderboard.commits_flat").fetchone()[
            0
        ]
        == 0
    )
    con.close()
