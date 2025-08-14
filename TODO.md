# TODO – Road‑map  (last updated: 2025-08-14)

> *Record only high‑level milestones here; break micro‑tasks out into Issues.*
> **When you finish a task, tick it and append a short NOTE entry
> (see NOTES.md).**
> Keep this list ordered by topic and **never reorder past items**.

## 0 · Project bootstrap
- [x] Configure `make lint` and `make test` (cover every language tool‑chain)
- [x] Commit starter governance files (`AGENTS.md`, `TODO.md`, `NOTES.md`,
- [x] Add `.codex/setup.sh`; ensure it is idempotent and exits 0
- [x] Audit repository & docs; identify the single source of truth
       (spec, assignment …) and reference it in README
- [x] Generate initial dependency manifests (`requirements.txt`,
      `package.json`, `pubspec.yaml`, …) with pinned versions
- [ ] Define ownership of all generated code in `/generated/**` and record the
      regeneration command in `AGENTS.md`
- [x] Push the first green CI run (docs‑only + full‑tests job)

## 1 · Core functionality

Repeat the five‑bullet block below for every MVP feature A, B, C, …

- [x] Analyse source‑of‑truth docs; define acceptance criteria for
      **GitHub commits pipeline**
  - [x] Document assumptions / edge‑cases for GitHub commits pipeline in
    `/docs` or README
  - [x] Implement GitHub commits pipeline
- [x] Add unit / integration tests for GitHub commits pipeline
- [x] Wire CI quality gate (coverage ≥ 80 %, metric thresholds, etc.) that
      exits 1 on regression

## 2 · Documentation & CI

- [x] Write README quick‑start (clone → setup → test)
- [ ] Add full doc build (Sphinx / JSDoc / dart‑doc as applicable)
- [x] Integrate secret‑detection helper step in CI (`has_token` pattern)
- [ ] Extend CI matrix for all runtimes (Python, Node, Dart, Rust, …)
- [x] Add Actionlint job and pin markdownlint-cli version
- [ ] Add markdown-link-check job and pin its version
- [ ] Publish docs to GitHub Pages when `GH_PAGES_TOKEN` is present

## 3 · Quality & automation

- [x] Add pre‑commit hooks (formatters, linters, markdownlint, actionlint)
- [x] Enforce coverage threshold (≥ 80 % branch, exclude `/generated/**`)
- [ ] Add linters for conflict markers, trailing spaces and NOTES ordering
- [ ] Introduce dependabot / Renovate with the version‑pin policy from
      `AGENTS.md`

## 4 · Stretch goals

- [ ] Containerise dev environment (Dockerfile or dev‑container.json)
- [ ] Auto‑deploy docs & storybooks on each tag
- [ ] Publish packages (PyPI, npm, pub.dev) via release workflow
- [ ] Add optional load‑testing / performance CI stage

---

### Add new items below this line
*(append only; keep earlier history intact)*
- [x] Add `.gitignore` for DLT state, DuckDB, venv, caches (2025-08-11)
- [x] Require `make test` to fail when no tests are collected (2025-08-11)
- [x] Ensure `.codex/setup.sh` creates `.venv` with lint tools (2025-08-11)
- [x] Implement GitHub leaderboard pipeline in `src/gh_leaderboard`
- [x] Fix markdownlint errors across docs to make `lint-docs` job pass
- [x] Add DuckDB destination and post-load SQL for leaderboard
- [x] Pin `requests` dependency for HTTP calls (2025-08-11)
- [x] Allow `make test` to forward flags like `--offline` to pytest (2025-08-11)
- [x] Review dlt pipelines per `docs/dlt_guide_for_codex_2025.txt` (2025-08-11)
- [x] Wrap lint and test commands in `AGENTS.md` code fence (2025-08-11)
- [x] Replace `grep` with anchored `git grep` for conflict checks (2025-08-11)
- [x] Revise conflict marker guidelines using placeholders in AGENTS.md (2025-08-12)
- [x] Add markdownlint and actionlint to pre-commit config (2025-08-12)
- [x] Run pre-commit hooks via `pre-commit run --all-files` in Makefile and CI
      (2025-08-12)
- [x] Add `check-merge-conflict` hook to pre-commit config (2025-08-12)
- [x] Add tests for offline edge cases and handle empty commit fixtures
      (2025-08-12)
- [x] Add tests for GitHub commits source headers and params (2025-08-12)
- [x] Audit other normalization helpers for whitespace handling (2025-08-12)
- [x] Audit tests to ensure network calls are mocked or use offline fixtures (2025-08-12)
- [x] Add tests for `flatten_commit` missing commit date (2025-08-12)
- [x] Add unit test for `commits_flat` transformer (2025-08-12)
- [x] Test incremental cursor uses last_value and omits auth header
when token missing (2025-08-12)
- [x] Increase coverage threshold to ≥ 90 % (2025-08-12)
- [x] Extend `flatten_commit` tests for missing login and commit key (2025-08-12)
- [x] Add test for pipeline default DuckDB path when `pipelines_dir` is omitted (2025-08-12)
- [x] Test `github_commits_source` base URL and per_page=100 (2025-08-12)
- [x] Handle missing or invalid fixture file gracefully in pipeline run (2025-08-12)
- [x] Add test verifying author date fallback when committer date is missing
      (2025-08-12)
- [x] Log or surface skipped commits lacking timestamps (2025-08-12)
- [x] Add tests for `normalize_author` handling blank email cases (2025-08-12)
- [x] Ensure pipeline ignores fixture files that aren't lists (2025-08-12)
- [x] Guard `flatten_commit` against `None` committer blocks and add tests (2025-08-12)
- [x] Test incremental cursor uses initial_value when state is empty (2025-08-12)
- [x] Ensure `pipeline.run` writes DuckDB to current directory when `pipelines_dir` is omitted (2025-08-12)
- [x] Add multi-day commit fixture and post-load grouping test (2025-08-12)
- [x] Rename commit resource to `commits_raw` and update references (2025-08-13)
- [x] Expand `flatten_commit` with author metadata fields and `message_short` and update tests (2025-08-13)
- [x] Load default commit fixture when `fixture_path` is None (2025-08-13)
- [x] Create `leaderboard_latest` view and add tests (2025-08-13)
- [x] Add CLI config loader for repo and date window (2025-08-13)
- [x] Add integration test for CLI entry (2025-08-13)
- [x] Ensure incremental cursor falls back to author date when committer date is
      missing (2025-08-13)
- [x] Document `leaderboard_latest` view in README and examples (2025-08-13)
- [x] Rename dataset to `github_leaderboard` across code and docs (2025-08-13)
- [x] Correct documentation to reference `leaderboard.duckdb` file name (2025-08-13)
- [x] Document troubleshooting tips for common pipeline errors in README
      (2025-08-13)
- [x] Add `.dlt/secrets.toml` to `.gitignore` and warn against committing
      secrets (2025-08-13)
- [x] Rename offline pipeline test with e2e tag and document run command (2025-08-13)
- [x] Handle GitHub API 403 errors with RuntimeError and tests (2025-08-13)
- [x] Ensure pipeline creates empty commit tables when no commits are loaded (2025-08-13)
- [x] Document full refresh workflow for DuckDB in README and AGENTS (2025-08-13)
- [x] Normalize commit timestamps to UTC and derive commit_day from UTC (2025-08-13)
- [x] Load GitHub token from .dlt/secrets.toml and compute window_days defaults (2025-08-13)
- [x] Pass Settings.token through pipeline instead of env var (2025-08-13)
- [x] Rename config section from `[gh_leaderboard]` to `[gh]` and verify loader (2025-08-13)
- [x] Deduplicate commits by SHA when loading commits_flat (2025-08-13)
- [x] Add live pipeline test with closed window and README instructions (2025-08-13)
- [x] Add test ensuring pipeline idempotent when re-run with same data (2025-08-13)
- [x] Add online pipeline idempotency test using RESTClient stub (2025-08-13)
- [x] Document `write_disposition="merge"` requirement for primary-key dlt
      resources (2025-08-14)
- [x] Ensure online pipeline deduplicates commits by SHA via merge (2025-08-13)
- [x] Add safety overlap and merge for idempotency (2025-08-14)
- [x] Implement retry/backoff for GitHub rate limits (2025-08-14)
- [ ] Support BigQuery or Snowflake destinations (2025-08-14)
- [ ] Surface richer metrics and dashboards (2025-08-14)
- [ ] Schedule pipeline runs via cron or GitHub Actions (2025-08-14)
- [x] Overlap incremental cursor by 60s and update tests (2025-08-14)
- [x] Clarify idempotent reruns and 60s cursor overlap in docs (2025-08-14)
- [x] Deduplicate `commits_raw` by SHA and test row count stability (2025-08-14)
- [x] Retry 502/503/504 and network timeouts with jittered backoff (2025-08-14)
- [ ] Expose retry metrics and allow configuring backoff parameters (2025-08-14)
