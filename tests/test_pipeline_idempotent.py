from pathlib import Path

import dlt

from src.gh_leaderboard import pipeline


def test_pipeline_idempotent(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "commits.json"
    pipeline.run(offline=True, fixture_path=fixture, pipelines_dir=tmp_path)
    p = dlt.pipeline(
        "gh_leaderboard",
        destination=dlt.destinations.duckdb(
            str(tmp_path / "leaderboard.duckdb"),
        ),
        dataset_name="github_leaderboard",
        pipelines_dir=str(tmp_path),
    )
    with p.sql_client() as sql:
        before_leader = sql.execute_sql(
            "select count(*) from leaderboard_daily",
        )[
            0
        ][0]
        before_raw = sql.execute_sql(
            "select count(*) from commits_raw",
        )[
            0
        ][0]
    pipeline.run(offline=True, fixture_path=fixture, pipelines_dir=tmp_path)
    with p.sql_client() as sql:
        after_leader = sql.execute_sql(
            "select count(*) from leaderboard_daily",
        )[
            0
        ][0]
        after_raw = sql.execute_sql(
            "select count(*) from commits_raw",
        )[
            0
        ][0]
        total, distinct_sha = sql.execute_sql(
            """
            select count(*) as total, count(distinct cf.sha) as distinct_sha
            from leaderboard_daily ld
            join commits_flat cf
            on ld.author_identity = cf.author_identity
            and ld.commit_day = cf.commit_day
            """,
        )[0]
    assert before_leader == after_leader
    assert total == distinct_sha
    assert before_raw == after_raw
