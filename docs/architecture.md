Architecture Overview

Components

- Config: `chat_history_manager.config`

  - Env-first settings with `${VAR}` and `${VAR:-default}` interpolation.
  - Per-OS default storage path if unset.
  - Index file path derived from base dir.

- Secrets Provider: `chat_history_manager.secrets_provider`

  - Chain: Environment → OS keychain (`keyring` optional extra).
  - Used by config interpolation; safe for prototyping.

- Data Model: `chat_history_manager.models.IndexEntry`

  - Pydantic model for the index entries (schema + validation).

- Utilities: `chat_history_manager.utils`

  - Directory management, chunk IO, index read/update, chunk sizing.

- Domain API: `chat_history_manager.main`

  - `save_chat_history`: create Markdown chunk + update index.
  - `retrieve_chat_history`: filter and return latest chunk contents.

- CLI: `chat_history_manager.cli`

  - `save` (stdin or file) and `retrieve` (filters, limit) subcommands.

Storage Model

- Markdown chunks: `chat_history_00001.md`, ...
- JSON index: `chat_history_index.json` (newest-first entries).

Operational Concerns

- Config & Secrets: No committed personal configs; use env or keychain.
- Portability: Works out-of-the-box with per-OS defaults.
- CI: Conventional Commits checks, tests on multiple Python versions, ruff lint/format.
