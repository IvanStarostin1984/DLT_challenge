#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "${REPO_ROOT}/.venv" ]; then
    python -m venv "${REPO_ROOT}/.venv"
fi

"${REPO_ROOT}/.venv/bin/pip" install -r "${REPO_ROOT}/requirements.txt"

# install git hooks when configuration is present
if [ -f "${REPO_ROOT}/.pre-commit-config.yaml" ]; then
    "${REPO_ROOT}/.venv/bin/pre-commit" install
fi

exit 0
