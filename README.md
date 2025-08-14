# GitHub commit leaderboard pipeline

This project is a small [dlt](https://dlthub.com/) pipeline that loads recent
GitHub commits into DuckDB and builds a daily leaderboard of contributors.

See [docs/specs.txt](docs/specs.txt) for the master specification and
[docs/acceptance_criteria.md](docs/acceptance_criteria.md) for goals and
edge cases.

It creates three tables and one view:

* `commits_raw`
* `commits_flat`
* `leaderboard_daily`
* `leaderboard_latest` – view of the last 1–2 days

## Quick start (Windows PowerShell)

1. `cd DLT_challenge`
2. `py -m venv .venv`
3. `. .\\.venv\\Scripts\\Activate.ps1`
4. `pip install -r requirements.txt`
5. `python -m src.gh_leaderboard.pipeline`
6. Inspect results:

   ```python
   import dlt

   p = dlt.pipeline("gh_leaderboard")
   with p.sql_client() as sql:
       print(sql.execute_sql("select * from leaderboard_daily"))
       print(sql.execute_sql("select * from leaderboard_latest"))
   ```

## Quick start (Linux / macOS / WSL)

1. `cd DLT_challenge`
2. `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python -m src.gh_leaderboard.pipeline`
6. Inspect results:

   ```python
   import dlt

   p = dlt.pipeline("gh_leaderboard")
   with p.sql_client() as sql:
       print(sql.execute_sql("select * from leaderboard_daily"))
       print(sql.execute_sql("select * from leaderboard_latest"))
   ```

Set `GITHUB_TOKEN` or add `[github].token` to `.dlt/secrets.toml` to raise rate
limits if needed.

Defaults for repository, branch and date window come from `[gh]` in
`.dlt/config.toml` or environment variables `GH_REPO`, `GH_BRANCH`, `GH_SINCE_ISO`,
`GH_UNTIL_ISO`. Command line flags override these values:

```bash
python -m src.gh_leaderboard.pipeline --repo my/repo --offline
```

## Usage

```python
from src.gh_leaderboard import pipeline
import dlt

rows = pipeline.run(
    repo="octocat/Hello-World",
    since="2012-03-06T00:00:00Z",
    until="2012-03-07T00:00:00Z",
)
p = dlt.pipeline(
    "gh_leaderboard", destination="duckdb", dataset_name="github_leaderboard"
)
with p.sql_client() as sql:
    print(
        sql.execute_sql(
            "select * from leaderboard_daily order by author_identity"
        )
    )
    print(sql.execute_sql("select * from leaderboard_latest"))
```

Each row has `author_identity`, `commit_day`, and `commit_count`. Use
`offline=True` to read the bundled fixture instead of hitting GitHub. When the
fixture file is missing or malformed JSON the pipeline returns an empty list.
The results are stored in `leaderboard.duckdb` with tables `commits_raw`,
`commits_flat`, `leaderboard_daily`, and the `leaderboard_latest` view.
Even when no commits are loaded, the `commits_raw` and `commits_flat` tables are
created with zero rows.

## Offline workflow

Running offline loads the sample fixture at `fixtures/commits_sample.json`:

```python
from src.gh_leaderboard import pipeline

rows = pipeline.run(offline=True)
```

Pass `fixture_path` to load a different JSON file.

## Deduplication

The pipeline merges commits sharing the same `sha`.
Offline runs pass `primary_key="sha"` with `write_disposition="merge"` so
duplicate rows do not inflate `leaderboard_daily` counts.

## Linting

Run all pre-commit hooks before committing:

```bash
pre-commit run --all-files
```

## Tests

Run unit and end-to-end tests:

```bash
make test
```

Forward extra flags with `PYTEST_ARGS`. For example, skip network tests:

```bash
make test PYTEST_ARGS="--offline"
```

The live pipeline test needs a `GITHUB_TOKEN`. Run it explicitly with the
`live` marker:

```bash
GITHUB_TOKEN=... pytest -m live tests/test_pipeline.py
```

## Common issues

* 403 or pagination stalls → set `GITHUB_TOKEN`; ensure `per_page=100`.
* Empty results → adjust `--since/--until`; confirm branch.
* Codex: no internet → use `--offline`.

Run just the offline end-to-end test:

```bash
pytest -q -k e2e --offline
```
## Incremental loads

The resource uses `commit.committer.date` as the cursor and falls back to
`commit.author.date` when the committer date is missing. dlt stores the last
cursor so pass `--since` on the next run.

### Full refresh

To rebuild the database, drop the DuckDB tables and rerun the pipeline with a
far‑past `--since` date. This clears incremental state and reloads all commits.

```bash
python -m src.gh_leaderboard.pipeline --since "1970-01-01T00:00:00Z"
```

## Troubleshooting

### HTTP 403 from GitHub

`commits_raw` logs an error and raises `RuntimeError` when the API responds
with 403. Check the `GITHUB_TOKEN`, ensure the repo is accessible, and retry
after the rate limit resets.

## Design decisions

### Why GitHub API

GitHub's REST API is stable, well documented, and Link headers simplify
pagination. Rate limits are predictable, and commit timestamps enable
incremental loads with daily rollups.

### What next with more time

Safety overlap and merge already keep loads idempotent. With more time we
would add retry with backoff for rate limits, target BigQuery or
Snowflake, surface richer metrics and dashboards, and schedule runs via
cron or GitHub Actions.
