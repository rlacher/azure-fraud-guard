#!/usr/bin/env bash
set -euo pipefail

ARCHIVE_NAME="azure-fraud-guard.tar.gz"

if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "Error: Not inside a git repository." >&2
  exit 1
fi

git ls-files -z | tar --null -T - -czf "$ARCHIVE_NAME"

echo "Created archive: $ARCHIVE_NAME"
