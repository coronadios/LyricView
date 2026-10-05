#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="/usr/local/bin/lv"

if [[ ! -f "$ROOT_DIR/lv" ]]; then
  echo "Missing launcher at $ROOT_DIR/lv"
  exit 1
fi

cp "$ROOT_DIR/lv" "$TARGET"
chmod +x "$TARGET"

echo "LyricView installed to $TARGET"
echo "Example: lv -test --file \"$ROOT_DIR/lyric-test.txt\" --theme:aurora"
