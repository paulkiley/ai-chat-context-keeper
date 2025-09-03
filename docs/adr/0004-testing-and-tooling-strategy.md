# 4. Testing and Tooling Strategy

Date: 2025-09-03

## Status

Accepted

## Context

We need a modern, fast developer workflow with robust testing and linting, and consistent environments.

## Decision

Adopt:

- `uv` for venv and dependency management.
- `pytest` for tests with coverage ≥85%.
- `ruff` for lint and format.
- `pre-commit` hooks for local enforcement.
- CI workflows for tests (matrix) and lint.

## Consequences

### Positive

- Fast feedback loops; consistent style and quality.
- Clear, enforceable quality bars in CI.

### Negative

- Additional tooling to install locally.

