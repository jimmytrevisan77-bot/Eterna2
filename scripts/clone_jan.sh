#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/janhq/jan.git"
TARGET_DIR="jan"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "Jan repository already cloned at $TARGET_DIR" >&2
  exit 0
fi

if ! command -v git >/dev/null 2>&1; then
  echo "git command is required to clone Jan" >&2
  exit 1
fi

echo "Cloning Jan from $REPO_URL into $TARGET_DIR" >&2
git clone "$REPO_URL" "$TARGET_DIR"
