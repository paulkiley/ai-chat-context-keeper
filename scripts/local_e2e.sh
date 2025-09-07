#!/usr/bin/env bash
set -euo pipefail

# Local end-to-end validation on macOS (works on Linux too).
# - Uses a temp directory for history storage.
# - Exercises save/retrieve and retention.

HERE=$(cd "$(dirname "$0")/.." && pwd)
cd "$HERE"

log() { printf "[e2e] %s\n" "$*"; }

PY=""
RUN() { # RUN <args...>    -> runs the CLI via selected runner
  if [[ -n "$PY" ]]; then
    "$PY" -m chat_history_manager.cli "$@"
  else
    uv run chatlog "$@"
  fi
}

# Choose runner: prefer local venv python; else uv; else create venv with python3.
if [[ -x .venv/bin/python ]]; then
  PY="$(pwd)/.venv/bin/python"
  log "Using existing venv: $PY"
else
  if command -v uv >/dev/null 2>&1; then
    log "Using uv to manage environment"
    uv venv >/dev/null
    uv pip install -q -e .[dev]
  else
    log "uv not found; falling back to python3 venv"
    python3 -m venv .venv
    .venv/bin/pip install -q -U pip
    .venv/bin/pip install -q -e .[dev]
    PY="$(pwd)/.venv/bin/python"
  fi
fi

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

export CHAT_HISTORY_BASE_DIR="$TMPDIR/history"
log "History dir: $CHAT_HISTORY_BASE_DIR"

log "Saving two chunks..."
echo "hello-1" | RUN save --project-name P --topic T1 --summary S1 >/dev/null
echo "hello-2" | RUN save --project-name P --topic T2 --summary S2 >/dev/null

log "Retrieving latest 2..."
OUT=$(RUN retrieve --project-name P --limit 2)
echo "$OUT" | grep -q "hello-2"
echo "$OUT" | grep -q "hello-1"

log "Applying retention: keep only newest 1"
export CHAT_RETENTION_MAX_CHUNKS=1
echo "hello-3" | RUN save --project-name P --topic T3 --summary S3 >/dev/null

OUT2=$(RUN retrieve --project-name P --limit 2)
echo "$OUT2" | grep -q "hello-3"
if echo "$OUT2" | grep -q "hello-2"; then
  echo "Expected older chunks pruned; found hello-2" >&2
  exit 1
fi

log "SUCCESS: local E2E passed"
