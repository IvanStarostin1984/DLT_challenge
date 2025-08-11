#!/usr/bin/env bash
set -euo pipefail

if [ -f requirements.txt ]; then
  pip install --requirement requirements.txt >/tmp/pip_install.log 2>&1 || cat /tmp/pip_install.log
fi

exit 0
