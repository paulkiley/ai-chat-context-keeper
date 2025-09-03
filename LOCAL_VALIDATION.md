Local Validation Guide (macOS)

Prereqs

- Python 3.10+ installed
- Optional: `uv` for fast venvs (brew install uv)

One-time setup

```sh
cd paulkiley/chat_history_manager
make install      # creates venv and installs dev deps
make hooks        # pre-commit hooks incl. commit-msg
```

Sanity checks

```sh
make lint         # ruff check
make format       # ruff format
make test         # pytest (>=85% coverage)
```

End-to-end test

```sh
make e2e
```

Manual smoke tests

```sh
# Use your existing history dir if desired
export CHAT_HISTORY_BASE_DIR="$HOME/workspace/github/gemini_chat_history"

# Save from clipboard (macOS)
pbpaste | uv run chatlog save --project-name MyProj --topic Setup --summary "From clipboard"

# Or save from file
uv run chatlog save --project-name MyProj --topic Setup --file README.md

# Retrieve latest
uv run chatlog retrieve --project-name MyProj --topic Setup --limit 2

# Test retention locally (optional)
export CHAT_RETENTION_MAX_CHUNKS=1
echo test | uv run chatlog save --project-name MyProj --topic Ret
uv run chatlog retrieve --project-name MyProj --limit 5
```

Docs locally (optional)

```sh
uv pip install -e .[docs]
make docs-serve  # http://localhost:8000
```

Keyring fallback (optional)

```sh
uv pip install -e .[secrets]
python - <<'PY'
import keyring; keyring.set_password('chat_history_manager','CHM_HISTORY_DIR','/tmp/chm')
PY
export CHAT_HISTORY_BASE_DIR='${CHM_HISTORY_DIR:-/tmp/chm-fallback}'
uv run chatlog retrieve --limit 1

Staging smoke test (safe write test)

```sh
# Copies your real folder to a staging directory, then writes one test record
# Defaults:
#   CHM_STAGE_SRC=$HOME/workspace/github/gemini_chat_history
#   CHM_STAGE_DIR=${CHM_STAGE_SRC}_staging

make smoke-staging

# Or override the source/destination
CHM_STAGE_SRC="/path/to/gemini_chat_history" \
CHM_STAGE_DIR="/tmp/gemini_chat_history_staging" \
make smoke-staging
```
```
