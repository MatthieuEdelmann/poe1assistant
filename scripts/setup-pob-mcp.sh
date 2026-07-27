#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/pob-mcp"

if [[ ! -d "$VENDOR/.git" ]]; then
  git clone https://github.com/ianderse/pob-mcp.git "$VENDOR"
else
  echo "pob-mcp already cloned at $VENDOR"
fi

cd "$VENDOR"
npm install
npm run build

echo "Done. Update paths in $ROOT/.cursor/mcp.json if needed."
