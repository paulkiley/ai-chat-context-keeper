# CLI

Entry point: `chatlog`

Subcommands

- `save`
  - Required: `--project-name`, `--topic`
  - Optional: `--summary`, `--session-id`, `--keywords`, `--file`
  - Flags: `--dry-run` (preview without writing)
  - Content: read from `--file` or stdin
- `retrieve`
  - Optional filters: `--project-name`, `--topic`, `--session-id`
  - `--limit` (default 1)

Examples

```sh
pbpaste | uv run chatlog save --project-name Repo --topic Setup --summary "Install"
uv run chatlog retrieve --project-name Repo --topic Setup --limit 2

Read-only mode

- Set `CHM_READ_ONLY=1` to prevent writes. Combine with `--dry-run` to preview the next chunk path without modifying the index or files.
```
