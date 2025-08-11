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

## 2025-08-11  PR #1

- **Summary**: Added Makefile with lint and test targets wired to `.venv`.
- **Stage**: implementation
- **Motivation / Decision**: standardised quality gates; relaxed markdown rules
   to tolerate legacy docs.
- **Next step**: add setup script for installing the tool chain.

## 2025-08-11  PR #2

- **Summary**: Created gh_leaderboard package skeleton.
- **Stage**: planning
- **Motivation / Decision**: start structure for future dlt pipeline.
- **Next step**: implement GitHub commit pipeline.

## 2025-08-11  PR #3

- **Summary**: add CI workflow with docs-only and test paths.
- **Stage**: implementation
- **Motivation / Decision**: ensure docs edits run fast checks while code runs full tests.
- **Next step**: add `.codex/setup.sh` and wire `make lint` and `make test`.

## 2025-08-11  PR #4

- **Summary**: Expanded README with setup instructions, tests, and design notes.
- **Stage**: documentation
- **Motivation / Decision**: Align docs with specs to guide future work.
- **Next step**: Implement GitHub commits pipeline.

## 2025-08-11  PR #5

- **Summary**: added setup script and pinned dependency manifest.
- **Stage**: implementation
- **Motivation / Decision**: ensure consistent environment.
- **Next step**: configure lint and test commands.
