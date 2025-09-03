# Configuration

- Env-first configuration; no committed personal configs.
- Interpolation supports `${VAR}` and `${VAR:-default}`.
- Secrets provider chain: Environment → OS keychain (if `keyring` installed).

Defaults

- macOS: `~/Library/Application Support/chat_history_manager/history`
- Linux: `${XDG_DATA_HOME:-~/.local/share}/chat_history_manager/history`
- Windows: `~/AppData/Local/chat_history_manager/history`

Key variables

- `CHAT_HISTORY_BASE_DIR` – base folder for history/index
- `CHAT_RETENTION_MAX_CHUNKS` – keep only newest N chunks (optional)
- `CHAT_RETENTION_MAX_AGE_DAYS` – remove entries older than N days (optional)

Examples

```sh
export CHAT_HISTORY_BASE_DIR='${CHM_HISTORY_DIR:-${HOME}/.local/share/chat_history_manager/history}'
# set keyring value (macOS example)
python - <<'PY'
import keyring; keyring.set_password('chat_history_manager','CHM_HISTORY_DIR','/path/to/history')
PY
```

