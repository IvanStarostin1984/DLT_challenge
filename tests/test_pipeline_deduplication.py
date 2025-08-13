from pathlib import Path

import dlt

from src.gh_leaderboard import pipeline


def test_duplicates_are_merged(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "commits_duplicate_sha.json"
    pipeline.run(offline=True, fixture_path=fixture, pipelines_dir=tmp_path)
    p = dlt.pipeline(
        "gh_leaderboard",
        destination=dlt.destinations.duckdb(str(tmp_path / "leaderboard.duckdb")),
        dataset_name="github_leaderboard",
        pipelines_dir=str(tmp_path),
    )
    with p.sql_client() as sql:
        total, distinct_sha = sql.execute_sql(
            """
            select count(*) as total, count(distinct cf.sha) as distinct_sha
            from leaderboard_daily ld
            join commits_flat cf
            on ld.author_identity = cf.author_identity
            and ld.commit_day = cf.commit_day
            """
        )[0]
    assert total == distinct_sha
