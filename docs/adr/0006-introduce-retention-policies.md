# 6. Introduce Retention Policies

Date: 2025-09-03

## Status

Accepted

## Context

Long-running histories can grow unbounded. We need basic retention to prevent excessive storage usage without introducing a heavy dependency.

## Decision

Add optional retention policies configured via environment variables:

- `CHAT_RETENTION_MAX_CHUNKS`: keep only the newest N chunks.
- `CHAT_RETENTION_MAX_AGE_DAYS`: remove entries older than N days.

Retention runs after each save operation. The index is rewritten, and pruned chunk files are deleted.

## Consequences

### Positive

- Prevents unbounded growth with minimal complexity.
- Keeps newest context available by default.

### Negative

- Deletions are irreversible; backups/archives should be handled separately.
- Age-based pruning uses local time; future work could add UTC handling.
