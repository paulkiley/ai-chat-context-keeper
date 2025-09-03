# 8. Naming and Messaging Strategy

Date: 2025-09-03

## Status

Accepted

## Context

Names should clearly communicate the purpose of the project: resilient AI chat context capture and resumption. Repo naming should follow common OSS conventions (kebab-case), while Python packaging keeps snake_case imports. Environment variables should use a consistent, scoped prefix.

## Decision

1. Repository naming: use kebab-case `ai-chat-context-keeper` for the GitHub repository.
2. Python packaging: keep the import path `chat_history_manager`; set distribution/project name to `ai-chat-context-keeper`.
3. CLI: keep `chatlog` and add a short alias `chm`.
4. Environment variables: standardize on `CHM_…` prefix. Maintain backward compatibility with existing names during a deprecation window.
   - Preferred: `CHM_HISTORY_BASE_DIR`, `CHM_RETENTION_MAX_CHUNKS`, `CHM_RETENTION_MAX_AGE_DAYS`, `CHM_READ_ONLY`.
   - Compatibility: also read `CHAT_HISTORY_BASE_DIR`, `CHAT_RETENTION_*`, and `CHATLOG_READ_ONLY`.
5. Messaging: update README/docs to emphasize crash-safe capture and rapid resumption of AI chat context.

## Consequences

### Positive

- Clear purpose and CNCF-aligned neutral naming.
- Backward compatible transition for configuration.
- Better discoverability via repo name and docs.

### Negative

- Requires updating badges/links after repo rename.
- Two sets of env var names to support during deprecation.

