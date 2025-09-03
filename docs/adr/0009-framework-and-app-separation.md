# 9. Framework and App Separation

Date: 2025-09-03

## Status

Accepted

## Context

The framework (library + CLI) should evolve independently from applications consuming it. Clear versioning and boundaries improve stability, reuse, and upgrades.

## Decision

- Keep the framework in a dedicated repository (`ai-chat-context-keeper`) with SemVer tags and published artifacts.
- Provide an example application repository (`ai-chat-context-app-template`) that depends on the framework by version (or git tag) and demonstrates configuration via `CHM_*` environment variables.
- For development, allow either path editable installs or git-based installs; for CI/CD, pin exact framework versions.

## Consequences

### Positive

- Decoupled release cadence; easier upgrades and rollbacks for apps.
- Clearer ownership and scope boundaries.
- Encourages reuse across multiple applications.

### Negative

- Two repositories to maintain; coordination for cross-cutting changes.
- Requires publishing/tagging discipline in the framework.

