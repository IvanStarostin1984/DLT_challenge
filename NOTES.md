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

- **Summary**: Added coverage config and CI run with 80% threshold.
- **Stage**: maintenance
- **Motivation / Decision**: ensure tests measure code paths while excluding
  generated and test files.
- **Next step**: monitor coverage as features expand.

## 2025-08-11  PR #16

- **Summary**: Documented pipeline acceptance criteria and linked from README.
- **Stage**: documentation
- **Motivation / Decision**: clarify goals and close related TODO item.
- **Next step**: add DuckDB destination and post-load SQL for leaderboard.

## 2025-08-12  PR #17

- **Summary**: Added dlt source with incremental pagination and post-load SQL
  to materialise `leaderboard_daily` in DuckDB; updated tests and README.
- **Stage**: implementation
- **Motivation / Decision**: align pipeline with dlt best practices and make
  leaderboard queries reproducible.
- **Next step**: allow Makefile to forward pytest flags like `--offline`.
