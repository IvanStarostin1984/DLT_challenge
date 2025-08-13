# Engineering log  – append entries at **the end** (oldest → newest)

Each pull‑request **adds one new section** using the fixed template below.
*Never modify or reorder previous entries.*
Keep lines ≤ 80 chars and leave exactly **one blank line** between sections.

---

## TEMPLATE  (copy → fill → append)

### YYYY‑MM‑DD  PR #&lt;number or draft&gt;

- **Summary**: one‑sentence description of what changed.
- **Stage**: planning / implementation / testing / maintenance / release
- **Motivation / Decision**: why it was done, key trade‑offs.
- **Next step**: short pointer to planned follow‑up (if any).

---

## 2025‑01‑01  PR #0  🌱 *file created*

- **Summary**: Seeded repository with starter templates (`AGENTS.md`, `TODO.md`,
  `NOTES.md`) and minimal CI workflow.
- **Stage**: planning
- **Motivation / Decision**: establish collaboration conventions before code.
- **Next step**: set up lint/test commands and begin core feature A.

### 2025-08-11  PR #1

- **Summary**: Added `.gitignore` for DLT state, DuckDB, virtual env and caches.
- **Stage**: implementation
- **Motivation / Decision**: keep temporary files out of version control.
- **Next step**: prepare setup script and tooling for lint and tests.

## 2025-08-11  PR #2

- **Summary**: Added Makefile with lint and test targets wired to `.venv`.
- **Stage**: implementation
- **Motivation / Decision**: standardised quality gates; relaxed markdown rules
   to tolerate legacy docs.
- **Next step**: add setup script for installing the tool chain.

## 2025-08-11  PR #3

- **Summary**: Created gh_leaderboard package skeleton.
- **Stage**: planning
- **Motivation / Decision**: start structure for future dlt pipeline.
- **Next step**: implement GitHub commit pipeline.

## 2025-08-11  PR #4

- **Summary**: add CI workflow with docs-only and test paths.
- **Stage**: implementation
- **Motivation / Decision**: ensure docs edits run fast checks while code runs full tests.
- **Next step**: add `.codex/setup.sh` and wire `make lint` and `make test`.

## 2025-08-11  PR #5

- **Summary**: Expanded README with setup instructions, tests, and design notes.
- **Stage**: documentation
- **Motivation / Decision**: Align docs with specs to guide future work.
- **Next step**: Implement GitHub commits pipeline.

## 2025-08-11  PR #6

- **Summary**: added setup script and pinned dependency manifest.
- **Stage**: implementation
- **Motivation / Decision**: ensure consistent environment.
- **Next step**: configure lint and test commands.

## 2025-08-11  PR #7

- **Summary**: Documented that `make test` fails when no tests are collected and
  added a placeholder test.
- **Stage**: documentation
- **Motivation / Decision**: avoid false positives so contributors supply at
  least one test.
- **Next step**: expand test coverage for the GitHub leaderboard pipeline.

## 2025-08-11  PR #8

- **Summary**: Added unit and offline pipeline tests and tightened test target.
- **Stage**: testing
- **Motivation / Decision**: ensure pipeline can run on fixture and fail fast.
- **Next step**: implement live GitHub pipeline.

## 2025-08-11  PR #9

- **Summary**: Replaced placeholder repo path and linked master spec.
- **Stage**: documentation
- **Motivation / Decision**: keep instructions accurate and reference single source
  of truth.
- **Next step**: implement GitHub commits pipeline.

## 2025-08-11  PR #10

- **Summary**: `.codex/setup.sh` now provisions `.venv` with black and ruff so
  `make lint` runs.
- **Stage**: implementation
- **Motivation / Decision**: lint step failed due to missing virtual
  environment; installing tools in `.venv` isolates dependencies.
- **Next step**: run CI to confirm lint and tests pass.

## 2025-08-11  PR #11

- **Summary**: Enabled live GitHub calls with pagination and incremental state.
- **Stage**: implementation
- **Motivation / Decision**: Needed real data; used Link headers and stored the
  last cursor in a state file.
- **Next step**: Load results into DuckDB and build SQL leaderboard.

## 2025-08-11  PR #12

- **Summary**: Pinned `requests` dependency and documented ordered list style.
- **Stage**: maintenance
- **Motivation / Decision**: ensure stable HTTP client; clarify list numbering to satisfy markdownlint.
- **Next step**: apply `requests` in future pipeline features.

## 2025-08-11  PR #13

- **Summary**: Ran setup, fixed AGENTS numbering, and executed lint and tests offline/online.
- **Stage**: testing
- **Motivation / Decision**: verify tooling and document results; preparing for green CI.
- **Next step**: update Makefile to forward pytest flags.

## 2025-08-11  PR #14

- **Summary**: Bumped AGENTS guide to v1.6 and added dlt reference.
- **Stage**: documentation
- **Motivation / Decision**: centralise dlt practices using shared guide.
- **Next step**: follow guide when extending dlt pipelines.

## 2025-08-11  PR #15

- **Summary**: Forwarded pytest flags via `PYTEST_ARGS` and documented usage.
- **Stage**: implementation
- **Motivation / Decision**: allow offline runs from Makefile, closing TODO item.
- **Next step**: revisit if more pytest options are needed.

## 2025-08-11  PR #16

- **Summary**: Added coverage config and CI run with 80% threshold.
- **Stage**: maintenance
- **Motivation / Decision**: ensure tests measure code paths while excluding
  generated and test files.
- **Next step**: monitor coverage as features expand.

## 2025-08-11  PR #17

- **Summary**: Documented pipeline acceptance criteria and linked from README.
- **Stage**: documentation
- **Motivation / Decision**: clarify goals and close related TODO item.
- **Next step**: add DuckDB destination and post-load SQL for leaderboard.

## 2025-08-12  PR #18

- **Summary**: Added dlt source with incremental pagination and post-load SQL
  to materialise `leaderboard_daily` in DuckDB; updated tests and README.
- **Stage**: implementation
- **Motivation / Decision**: align pipeline with dlt best practices and make
  leaderboard queries reproducible.
- **Next step**: allow Makefile to forward pytest flags like `--offline`.

- 2025-08-11: Wrapped lint and test commands in `AGENTS.md` with a bash code
  block to remove a stray fence. Reason: keep contributor guide rendering clean
  and lint instructions accurate. Decisions: prefer explicit fenced block over
  omitting commands.

## 2025-08-11  PR #19

- **Summary**: Anchored conflict check with `git grep` and updated docs.
- **Stage**: maintenance
- **Motivation / Decision**: ensure conflict markers are caught while ignoring
  untracked files.
- **Next step**: consider adding pre-commit hooks for conflict markers.

## 2025-08-12  PR #20

- **Summary**: Clarified conflict marker checks and replaced markers with
  placeholders in AGENTS guide.
- **Stage**: documentation
- **Motivation / Decision**: prevent accidental markers and guide contributors
  to use placeholder regex.
- **Next step**: explore a pre-commit hook for conflict checks.

## 2025-08-12  PR #21

- **Summary**: Added pre-commit config with black, ruff, and basic checks.
- **Stage**: implementation
- **Motivation / Decision**: centralise formatting and linting to keep diffs
  small and catch whitespace issues early.
- **Next step**: add markdownlint and actionlint hooks.

## 2025-08-12  PR #22

- **Summary**: Linting now runs `pre-commit run --all-files` in Makefile and CI.
- **Stage**: maintenance
- **Motivation / Decision**: ensure all hooks run consistently across local
  and CI environments.
- **Next step**: extend pre-commit config with markdownlint and actionlint.

## 2025-08-12  PR #23

- **Summary**: Added merge-conflict check to pre-commit and updated guides.
- **Stage**: maintenance
- **Motivation / Decision**: catch conflict markers early with
  `check-merge-conflict` hook.
- **Next step**: monitor and extend hooks like markdownlint next.

## 2025-08-12  PR #24

- **Summary**: Added tests for offline edge cases and handled empty data.
- **Stage**: testing
- **Motivation / Decision**: Ensure pipeline handles missing dates and
  empty fixtures.
- **Next step**: watch for further edge cases.

## 2025-08-12  PR #25

- **Summary**: Added tests for GitHub commits source verifying headers and
  query parameters.
- **Stage**: testing
- **Motivation / Decision**: ensure token and incremental arguments reach the
  REST client; used monkeypatch with a stub for safety.
- **Next step**: add markdownlint and actionlint hooks.

## 2025-08-12  PR #26

- **Summary**: Added guideline to mock network calls in tests and updated roadmap.
- **Stage**: documentation
- **Motivation / Decision**: avoid flaky tests by forbidding live network access.
- **Next step**: audit tests for network mocking.

## 2025-08-12  PR #27

- **Summary**: Added tests for `normalize_author` case handling and trimmed login.
- **Stage**: testing
- **Motivation / Decision**: ensure author identities ignore blank login and
  case; chose simple strip-and-lower to avoid storing placeholders.
- **Next step**: audit other normalization helpers for similar whitespace bugs.

## 2025-08-12  PR #28

- **Summary**: Added unit tests for `flatten_commit` covering missing dates.
- **Stage**: testing
- **Motivation / Decision**: ensure commits without timestamps return `None`.
- **Next step**: broaden commit test scenarios.

## 2025-08-12  PR #29

- **Summary**: Added unit test for `commits_flat` transformer.
- **Stage**: testing
- **Motivation / Decision**: ensure transformer yields expected rows using a stub client.
- **Next step**: broaden commit scenarios for `commits_flat`.

## 2025-08-12  PR #30

- **Summary**: Added test ensuring cursor last_value is used,
auth header omitted without token, and `HeaderLinkPaginator` is invoked.
- **Stage**: testing
- **Motivation / Decision**: verify incremental state and header
handling for commit source using a stub REST client.
- **Next step**: continue auditing tests for network mocking.

## 2025-08-12  PR #31

- **Summary**: Raised coverage gate to 90% and synced CI docs.
- **Stage**: maintenance
- **Motivation / Decision**: align workflow with higher quality bar.
- **Next step**: monitor coverage as code expands.

## 2025-08-12  PR #32

- **Summary**: Extended `flatten_commit` tests and noted `python` alias
  requirement in `AGENTS.md`.
- **Stage**: testing
- **Motivation / Decision**: verify author fallback to email, handle malformed
  commits, and avoid setup failures when only `python3` exists.
- **Next step**: audit tests for other commit variants.

## 2025-08-12  PR #33

- **Summary**: Added test ensuring pipeline writes DuckDB
to CWD when `pipelines_dir` is omitted.
- **Stage**: testing
- **Motivation / Decision**: verify default path behavior
to avoid polluting repo root.
- **Next step**: add online test for default path handling.

## 2025-08-12  PR #34

- **Summary**: Added test verifying REST client base URL and default `per_page`.
- **Stage**: testing
- **Motivation / Decision**: ensure commits source hits repo endpoint and
  uses 100 items per page by default.
- **Next step**: audit tests for remaining REST client defaults.

## 2025-08-12  PR #35

- **Summary**: Wrapped fixture loading in error handling and added tests for
  missing or malformed JSON.
- **Stage**: implementation
- **Motivation / Decision**: prevent crashes when offline fixtures are absent
  or corrupt.
- **Next step**: review network mocking across remaining tests.

## 2025-08-12  PR #36

- **Summary**: Added test for author date fallback when committer date is missing.
- **Stage**: testing
- **Motivation / Decision**: confirm commits still flatten using author timestamp.
- **Next step**: review remaining commit variants for coverage.

## 2025-08-12  PR #37

- **Summary**: Added test for mixed commit timestamps so only dated commits
  aggregate.
- **Stage**: testing
- **Motivation / Decision**: ensure leaderboard ignores commits missing
  timestamps.
- **Next step**: surface skipped commits in future runs.

## 2025-08-12  PR #38

- **Summary**: Added tests for `normalize_author` with empty email cases.
- **Stage**: testing
- **Motivation / Decision**: ensure empty emails fall back to name or
  "unknown" to keep identity stable.
- **Next step**: review other normalizers for similar edge cases.

## 2025-08-12  PR #39

- **Summary**: Added test ensuring pipeline returns no rows and no DuckDB file
  when fixture JSON is not a list.
- **Stage**: testing
- **Motivation / Decision**: prevent stray tables from malformed fixtures;
  early exit keeps storage clean.
- **Next step**: document fixture format expectations.

## 2025-08-12  PR #40

- **Summary**: Guarded `flatten_commit` against `None` committers and unknown authors.
- **Stage**: implementation
- **Motivation / Decision**: prevent crashes from `None` in nested API responses;
  default missing author data to "unknown".
- **Next step**: audit other API fields for similar `None` checks.

## 2025-08-12  PR #41

- **Summary**: Added test ensuring initial cursor value sets `since` and omits auth header; fixed default DuckDB path.
- **Stage**: testing
- **Motivation / Decision**: verify pipeline uses `initial_value` when state is
  empty and avoids sending tokens; ensure `pipeline.run` writes database to the
  current directory.
- **Next step**: review other incremental scenarios.

## 2025-08-12  PR #42

- **Summary**: Added test for blank author name and made `normalize_author`
  return "unknown".
- **Stage**: testing
- **Motivation / Decision**: ensure whitespace-only names fall back to
  "unknown" per TODO.
- **Next step**: none.

## 2025-08-12  PR #43

- **Summary**: Added multi-day commit fixture and post-load grouping test.
- **Stage**: testing
- **Motivation / Decision**: verify leaderboard aggregates commits per day
  for one author.
- **Next step**: monitor for more grouping edge cases.

## 2025-08-12  PR #44

- **Summary**: Guarded commit flattening against non-dicts and logged missing timestamps.
- **Stage**: implementation
- **Motivation / Decision**: handle malformed API data and satisfy logging TODO.
- **Next step**: audit other pipeline stages for defensive parsing.

## 2025-08-12  PR #45

- **Summary**: Added test ensuring `run` forwards params and skipped live pipeline.
- **Stage**: testing
- **Motivation / Decision**: cover argument forwarding and remove network dependency for CI stability.
- **Next step**: audit other normalization helpers for whitespace handling.

## 2025-08-13  PR #46

- **Summary**: Renamed commits resource to `commits_raw` and updated tests and docs.
- **Stage**: implementation
- **Motivation / Decision**: clarify raw vs flattened table names for consistency.
- **Next step**: monitor downstream SQL for table name assumptions.

## 2025-08-12  PR #47

- **Summary**: Added markdownlint and actionlint hooks to pre-commit and
  reformatted a test.
- **Stage**: maintenance
- **Motivation / Decision**: pinned versions v0.45.0 and v1.7.7 to meet TODO.
- **Next step**: none.

## 2025-08-13  PR #48

- **Summary**: Exposed author metadata and short commit message in flattened rows.
- **Stage**: implementation
- **Motivation / Decision**: align `commits_flat` schema with spec for easier analysis.

## 2025-08-13  PR #49

- **Summary**: Added default commit fixture and offline path; updated docs and tests.
- **Stage**: implementation
- **Motivation / Decision**: allow offline runs without specifying fixture path.
- **Next step**: broaden sample fixtures for complex scenarios.

## 2025-08-13  PR #50

- **Summary**: Added `leaderboard_latest` view and tests covering last two days.
- **Stage**: implementation
- **Motivation / Decision**: expose recent activity and keep query simple by
  limiting to two days.

## 2025-08-13  PR #51

- **Summary**: Added config loader, `.dlt/config.toml`, CLI flags and tests.
- **Stage**: implementation
- **Motivation / Decision**: allow repo and date window overrides via file, env and CLI.
- **Next step**: none.

## 2025-08-13  PR #52

- **Summary**: Renamed dataset to `github_leaderboard` and updated code, tests, and docs.
- **Stage**: implementation
- **Motivation / Decision**: keep dataset naming consistent and adjust CLI test to accept data output.
- **Next step**: isolate CLI tests from shared pipeline state.
