# 7. Write Lock and Safety Flags (Read-only, Dry-run)

Date: 2025-09-03

## Status

Accepted

## Context

Accidental writes to production-like history folders and concurrent writers can corrupt data or cause loss. We need safeguards to support safe local validation and staged testing without sophisticated infrastructure.

## Decision

- Introduce a simple write lock around save operations (flock where available; fallback to exclusive file create). Remove the lockfile after operations.
- Add a read-only mode via environment flags (`CHM_READ_ONLY`, `CHATLOG_READ_ONLY`, or config `READ_ONLY`) that blocks writes unless `--dry-run` is used.
- Add `--dry-run` to `chatlog save` to preview the next chunk path and index entry without performing writes.

## Consequences

### Positive

- Reduces risk of concurrent write corruption.
- Enables safe testing against real directories (read-only + dry-run) and staging copies.
- Clear operational story for local-first workflows.

### Negative

- Locking semantics may vary on network filesystems; best-effort only.
- Additional code paths and flags to support, document, and test.
