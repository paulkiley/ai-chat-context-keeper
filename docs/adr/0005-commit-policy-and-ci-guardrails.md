# 5. Commit Policy and CI Guardrails

Date: 2025-09-03

## Status

Accepted

## Context

Readable history and safe merging practices are essential for collaboration and traceability across environments.

## Decision

Adopt Conventional Commits and atomic commits. Enforce via pre-commit/Commitizen locally and CI checks for commit messages and PR titles. Set commit header max length to 120 chars. Recommend required status checks on `main` for merges (commitlint, semantic PR title; optionally tests and lint).

## Consequences

### Positive

- Clean, searchable history and reliable automation.
- Consistency across contributors and tools.
- Flexible header length (120) balances clarity and concision.

### Negative

- Slight overhead for contributors to learn and adhere to the standard.
- Longer headers can still degrade readability if overused.
