# Contributor & CI Guide  <!-- AGENTS.md v1.10 -->

> **Read this file first** before opening a pull‑request.
> It defines the ground rules that keep humans, autonomous agents and
> CI in‑sync.
> If you change *any* rule below, **bump the version number in this heading**.

---
Always follow single source of truth (/docs/specs.txt).
Do as specified in signle source of truth (unless unable to implement).
There are 2 sections in single source of truth (/docs/specs.txt):
1. #Client specifications (not to be changed, read only).
2. #Detailed specifications (may be wrong, maybe changed as last resort).
If something is not specified in single source of truth - choose
simplest safest options.
Update TODO.md with what to do based on /docs/specs.txt.
Implement project as specified in TODO.md. Reflect on progress in NOTES.md.
When any issue in codex environment happens, always suggest
additions/modifications to this AGENTS.md to prevent such issues in
future.
Maintain and develop the project so that after each new feature user
will be able to download github repo and run in local IDE (Visual
Studion 2022 on Win 11) to test manually.

## 1 · File‑ownership & merge‑conflict safety

| Rule | Detail |
|------|--------|
| **Distinct‑files rule** | Every concurrent task **must** edit a unique |
| | list of non‑markdown files.<br>_Shared exceptions:_ anyone may |
| | **append** (never rewrite) `AGENTS.md`, `TODO.md`, `NOTES.md`. |
| **Append‑only logs** | `TODO.md` & `NOTES.md` are linear logs—never |
| | delete or reorder entries.<br>Add new items at the end of the |
| | file. |
| **Generated‑files rule** | Anything under `generated/**` or `openapi/**` |
| | is **code‑generated** – never hand‑edit; instead rerun the generator. |
| **Search for conflict markers** | Run `git grep -nE '^<{7}|^={7}|^>{7}' --` |
| | before every commit and make sure it finds nothing. |
| | Never write the conflict markers verbatim; use `<{7}`, `={7}`, or `>{7}` |
| | when referencing them. |

---

## 2 · Bootstrap (first‑run) checklist


1. Run `.codex/setup.sh` (or `./setup.sh`) once after cloning &
   whenever dependencies change.
   *The script creates `.venv/`, installs runtime, lint & test
   dependencies, and installs git hooks when `.pre-commit-config.yaml`
   is present.*
2. Create `.venv` (`python -m venv .venv`) and install deps:
   `.venv/bin/pip install -r requirements.txt`.
   Run `.codex/setup.sh` after activating; the Makefile uses `.venv/bin`.
   *The script installs language tool‑chains, pins versions and
   injects secrets.*
3. Export **required secrets** (`GIT_TOKEN`, `GH_PAGES_TOKEN`, …) in
   the repository/organisation **Secrets** console.
4. Verify the **secret‑detection helper step** in
   `.github/workflows/ci.yml` (see § 4) so forks without secrets
   still pass.
5. On the first PR, update README badges to point at your fork (owner/repo).

---

## 3 · What every contributor must know up‑front

1. **Branch & PR flow** – fork → `feat/<topic>` → PR into `main` (one
   reviewer required).
2. **Pre‑commit commands** (also run by CI):
   ```bash
   make lint                  # all format / static‑analysis steps
   make test [PYTEST_ARGS=...]# project’s unit-/integration tests
   ```

   * `make test` fails when no tests are collected; ensure at least one exists.
   * Pass flags to pytest via `PYTEST_ARGS`, e.g. `make test
     PYTEST_ARGS="--offline"`.

   ```bash
   make lint                      # all format / static‑analysis steps
   pytest --cov=src --cov-fail-under=80  # unit/integration tests w/ coverage
   ```

   * Coverage excludes `tests/**` and `generated/**` via `.coveragerc`.
   * `pytest` fails when no tests are collected; ensure at least one exists.

   Markdown lint rules live in `.markdownlint.json` for now.
3. **Test collection** – `make test` must fail if no tests are collected.
4. **Style rules** – keep code formatted (`black`, `prettier`,
   `dart format`, etc.) and Markdown lines ≤ 80 chars; exactly **one
   blank line** separates log entries.
5. **Exit‑code conventions** – scripts must exit ≠ 0 on failure so CI
   catches regressions (e.g. fail fast when quality gates or metric
   thresholds aren’t met).
6. **Version‑pin policy** – pin *major*/*minor* versions for critical
   runtimes & actions (e.g. `actions/checkout@v4`, `node@20`,
   `python~=3.11`).
7. **When docs change, update them everywhere** – if ambiguity arises,
   `/docs` overrides this file.
8. **Log discipline** – when a TODO item is ticked you **must** add
   the matching section in `NOTES.md` *in the same PR*; this keeps
   roadmap and log in‑sync.

---

## 4 · Lean but “fail‑fast” CI skeleton

`.github/workflows/ci.yml` — copy → adjust tool commands as needed.

```yaml
name: CI
on:
  pull_request:
  push:
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      md_only: ${{ steps.filter.outputs.md_only }}
    steps:
      - uses: actions/checkout@v4
      - id: filter
        uses: dorny/paths-filter@v3
        with:
          filters: |
            md_only:
              - '**/*.md'

  # --- helper step: detect secrets without using them in `if:` ---
  secret-check:
    runs-on: ubuntu-latest
    outputs:
      has_pages_token: ${{ steps.echo.outputs.has_pages }}
    steps:
        - id: echo         # returns 'true' / 'false'
          run: echo "has_pages=${{ secrets.GH_PAGES_TOKEN != '' }}" >> \
            $GITHUB_OUTPUT

  lint-docs:
    needs: [changes]
    if: needs.changes.outputs.md_only == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          npx --yes markdownlint-cli '**/*.md'
          git grep -nE '^<{7}|^={7}|^>{7}' -- && exit 1 || \
            echo "No conflict markers"

  test:
    needs: [changes]
    if: needs.changes.outputs.md_only != 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Bootstrap
        run: ./.codex/setup.sh   # idempotent; safe when absent
      - run: make lint
      - run: .venv/bin/pytest --cov=src --cov-fail-under=80
```

* **Docs‑only changes** run in seconds (`lint-docs`).
* **Code changes** run full lint + tests (`test`).
* Add job matrices (multi‑language), action‑lint, or deployment later—
  guardrails above already catch the 90 % most common issues.

---

## 5 · Coding & documentation style

* 4‑space indent (or 2‑spaces for JS/TS when enforced by the linter).
* ≤ 20 logical LOC per function, ≤ 2 nesting levels.
* Surround headings / lists / fenced code with a blank line
  (markdownlint MD022, MD032).
* Use `1.` for every item in ordered lists (markdownlint MD029).
* **No trailing spaces.** Run `git diff --check` or `make lint-docs`.
* Wrap identifiers like `__init__` in back‑ticks to avoid MD050.
* Each public API carries a short doc‑comment.
* Keep Markdown lines ≤ 80 chars to improve diff readability (tables
  may exceed if unavoidable).

### 5.1 Additional instructions:

* Any work involving dlt must consult `docs/dlt_guide_for_codex_2025.txt` for
  pipeline, resource, incremental-loading and pagination practices.
* Run `python -m src.gh_leaderboard.pipeline` to load commits into DuckDB and
  execute `post_load.sql` producing tables `commits`, `commits_flat`, and
  `leaderboard_daily`.

Code quality:
Clear, modular structure
Consistent formatting
Meaningful docstrings and comments
dlt usage:
Proper usage of dlt entities, such as sources, resources, transformers,
etc.
Use of incremental loading
Correct handling of pagination
Tests:
One well-written unit test for an individual function or small component
One comprehensive test that runs your dlt pipeline end to end (you
decide which invariants must hold and why)
Documentation:
A README.md that explains how to set up, run, and test the project
A short design decisions section (why this API, how you chose
incremental fields, what you’d do next with more time)
Reproducibility:
We should be able to clone your repo and run the pipeline end to end
Using a public API is recommended
Pin your dependencies

---

## 6 · How to update these rules

* Edit **only what you need**, append a dated bullet in `NOTES.md`,
  **bump the version number** at the top of this file, and open a PR.
* When CI tooling changes (new Action versions, new secrets, extra
  language runners) **update both** this guide **and** the workflow
  file in the **same PR**.

Happy shipping 🚀
