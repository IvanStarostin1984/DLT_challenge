# GitHub commit leaderboard pipeline

This project is a small [dlt](https://dlthub.com/) pipeline that loads recent
GitHub commits into DuckDB and builds a daily leaderboard of contributors.

See [docs/specs.txt](docs/specs.txt) for the master specification and
[docs/acceptance_criteria.md](docs/acceptance_criteria.md) for goals and
edge cases.

It creates three tables:

* `commits_raw`
* `commits_flat`
* `leaderboard_daily`

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
   ```

Set `GITHUB_TOKEN` to raise rate limits if needed.

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
    "gh_leaderboard", destination="duckdb", dataset_name="gh_leaderboard"
)
with p.sql_client() as sql:
    print(
        sql.execute_sql(
            "select * from leaderboard_daily order by author_identity"
        )
    )
```

Each row has `author_identity`, `commit_day`, and `commit_count`. Use
`offline=True` to read the bundled fixture instead of hitting GitHub. The
results are stored in `gh_leaderboard.duckdb` with tables `commits`,
`commits_flat`, and `leaderboard_daily`.

## Tests

Run unit and end-to-end tests:

```bash
make test
```

Forward extra flags with `PYTEST_ARGS`. For example, skip network tests:

```bash
make test PYTEST_ARGS="--offline"
```

## Incremental loads

The resource uses `commit.committer.date` as the cursor and falls back to the
author date. dlt stores the last cursor so pass `--since` on the next run.

## Design decisions

* Local DuckDB keeps dependencies minimal.
* Link header pagination walks through commit pages.
* The cursor uses commit times to enable incremental syncs.
* Author identity falls back from login to email to name.
