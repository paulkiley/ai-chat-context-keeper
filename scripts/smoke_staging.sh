#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")/.." && pwd)
cd "$HERE"

SRC=${CHM_STAGE_SRC:-"$HOME/workspace/github/gemini_chat_history"}
DST=${CHM_STAGE_DIR:-"${SRC}_staging"}

echo "[staging] source: $SRC"
echo "[staging] staging: $DST"

if [[ ! -d "$SRC" ]]; then
  echo "Source directory not found: $SRC" >&2
  exit 2
fi

mkdir -p "$DST"
rsync -a --delete "$SRC/" "$DST/"

export CHAT_HISTORY_BASE_DIR="$DST"
printf 'staging smoke %s\n' "$(date)" | uv run chatlog save --project-name Z_TEST --topic SMOKE --summary "staging smoke" >/dev/null
uv run chatlog retrieve --project-name Z_TEST --topic SMOKE --limit 1

echo "[staging] Success"

