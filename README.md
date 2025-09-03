AI Chat Context Keeper

[![commitlint](https://github.com/paulkiley/chat_history_manager/actions/workflows/commitlint.yml/badge.svg)](https://github.com/paulkiley/chat_history_manager/actions/workflows/commitlint.yml)
[![semantic-pr-title](https://github.com/paulkiley/chat_history_manager/actions/workflows/semantic-pr.yml/badge.svg)](https://github.com/paulkiley/chat_history_manager/actions/workflows/semantic-pr.yml)
[![python-tests](https://github.com/paulkiley/chat_history_manager/actions/workflows/python-tests.yml/badge.svg)](https://github.com/paulkiley/chat_history_manager/actions/workflows/python-tests.yml)
[![python-lint](https://github.com/paulkiley/chat_history_manager/actions/workflows/python-lint.yml/badge.svg)](https://github.com/paulkiley/chat_history_manager/actions/workflows/python-lint.yml)

Never lose your AI chat context again. This tool captures resilient chunks of your conversations and maintains a searchable index so crashes, refreshes, or session resets don’t erase your progress.

Quick Start

- Create venv: `uv venv` (or use your existing `.venv`)
- Install: `uv pip install -e .[dev]`
- Optional: `uv pip install .[secrets]` to enable OS keychain integration via `keyring`.
- Enable hooks: `pre-commit install && pre-commit install --hook-type commit-msg`
  - Lint/format: `pre-commit run -a`
 - Makefile shortcuts: `make lint | make format | make test | make ci`

CLI

- Save from stdin: `pbpaste | uv run chatlog save --project-name MyProj --topic Setup --summary "Initial setup"`
- Save from file: `uv run chatlog save --project-name MyProj --topic Setup --file notes.txt`
- Retrieve latest: `uv run chatlog retrieve --project-name MyProj --topic Setup --limit 3`
 - Dry-run preview (no writes): `pbpaste | uv run chatlog save --project-name MyProj --topic Setup --dry-run`
 - Alias: `uv run chm ...` works the same as `chatlog`

Configuration (CNCF-aligned)

- No committed personal config: This repo contains no project-specific paths or secrets.
- Env-first: Configure with environment variables (12-factor).
- Interpolation: `${VAR}` and `${VAR:-default}` with optional OS keychain fallback.
- Preferred env prefix: `CHM_…` (compat with existing `CHAT_*` / `CHATLOG_*`).
  - Example: `export CHM_HISTORY_BASE_DIR='${CHM_HISTORY_DIR:-${HOME}/.local/share/chat_history_manager/history}'`
  - Keychain example (macOS): `python -m keyring set chat_history_manager CHM_HISTORY_DIR` then enter the path.
- Defaults: If unset, a sensible per-OS default is used:
  - macOS: `~/Library/Application Support/chat_history_manager/history`
  - Linux: `${XDG_DATA_HOME:-~/.local/share}/chat_history_manager/history`
  - Windows: `~/AppData/Local/chat_history_manager/history`

Secrets (prototype-friendly)

- Provider chain: Env vars → OS keychain (`keyring`) if installed.
- Get a secret from keychain: `python - <<'PY'\nimport keyring; keyring.set_password('chat_history_manager','MY_TOKEN','<value>')\nPY`
- Access in code: `from chat_history_manager.secrets_provider import get_secret`.
- Do not commit `.env`: It’s gitignored by default. Prefer OS keychain for sensitive values even in dev.

Notes

- This package does not currently require any secrets. The provider is included for future integrations (e.g., cloud storage, APIs).
- For Kubernetes: use External Secrets Operator to sync cloud secrets (AWS/GCP/Vault) to env or mounted files; keep values out of images and Git.

Contributing

- See `CONTRIBUTING.md` for atomic/Conventional Commits policy, local tooling, and how to enable required status checks on `main`.
  - Style: `ruff check .` and `ruff format .`
  - Makefile: `make help`

Documentation

- Architecture: `docs/architecture.md`
- Development: `docs/development.md`
- ADRs: `docs/adr/`
 - Docs site (MkDocs): build locally with `make docs-build` or serve with `make docs-serve`. CI publishes to GitHub Pages (enable Pages for the repo).
 - Roadmap: `ROADMAP.md`
 - Known issues: `KNOWN_ISSUES.md`
 - Security advisories: `SECURITY_ADVISORIES.md`
 - Release notes: `releases/`

Retention

- Optional environment variables:
  - `CHAT_RETENTION_MAX_CHUNKS` – keep newest N chunks
  - `CHAT_RETENTION_MAX_AGE_DAYS` – delete entries older than N days

Safety options

- Read-only mode: set `CHM_READ_ONLY=1` to prevent writes (use with `--dry-run`).
- Staging smoke test: `make smoke-staging` copies your real folder to a staging directory and writes a single namespaced test entry (safe).

Current Scope

- Local-first chat history capture and retrieval via CLI.
- Markdown chunks + JSON index with simple filters (project/topic/session).
- Configuration via environment with interpolation; optional keyring fallback.
- Quality gates (tests, lint) and docs-as-code with ADRs.

Naming & Compatibility

- Repo: to be renamed to `ai-chat-context-keeper`.
- Python import path stays `chat_history_manager`; distribution name becomes `ai-chat-context-keeper`.
- CLI aliases: `chatlog` and `chm`.
- Env vars: prefer `CHM_*`; legacy `CHAT_*` and `CHATLOG_*` remain supported during a deprecation window.

Conventional Commits & Atomic History

- Local enforcement: `pre-commit install --hook-type commit-msg` enforces commit message format.
- Make commits via Commitizen: `cz commit` (guided prompts) and `cz bump` (version + changelog).
- PR title check: GitHub Action validates PR titles follow Conventional Commits.
- Common types: `feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert`.

Clean Up History (example)

- Use interactive rebase to squash fixups into a single atomic change:
  - `git rebase -i origin/main`
  - Mark small follow-ups as `fixup` or `squash` under the main commit.
  - Force-push your branch if needed: `git push -f`.
