#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "${REPO_ROOT}/.venv" ]; then
    python -m venv "${REPO_ROOT}/.venv"
fi

"${REPO_ROOT}/.venv/bin/pip" install -r "${REPO_ROOT}/requirements.txt"

exit 0
