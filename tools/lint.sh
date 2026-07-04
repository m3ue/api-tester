#!/usr/bin/env bash
# Fix lint issues and format code.
# Usage: ./tools/lint.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v ruff &>/dev/null; then
    echo "ruff not found. Install it with: pip install ruff"
    exit 1
fi

echo "Fixing lint issues..."
ruff check --fix --unsafe-fixes app/ tests/

echo "Formatting code..."
ruff format app/ tests/

echo "Done."
