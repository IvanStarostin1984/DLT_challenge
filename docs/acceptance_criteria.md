# Acceptance criteria – GitHub commits pipeline

## Functional goals

- Load commits from a chosen GitHub repository into DuckDB.
- Build a daily leaderboard that counts commits per author.
- Offer an offline mode that reads bundled fixture data.

## Success conditions

- All commit pages are fetched for the requested window.
- `leaderboard_daily` reflects the commit totals per author.
- A rerun with `--since` only processes new commits.

## Edge cases

- Hitting API rate limits reports a clear error and exits.
- Missing author info falls back to email or name fields.
- An empty time window still creates empty output tables.

## Testing

Run the offline end-to-end check:

```bash
pytest -q -k e2e --offline
```
