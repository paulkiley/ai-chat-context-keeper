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
- `ruff` for lint and format, with line length set to 120.
- `pre-commit` hooks for local enforcement (ruff, commit-msg via Commitizen/commitlint).
- CI workflows for tests (matrix) and lint. In CI, run `ruff check --fix` and `ruff format` before strict checks to reduce noise on PRs (auto-fixes are not pushed).

## Consequences

### Positive

- Fast feedback loops; consistent style and quality.
- Clear, enforceable quality bars in CI.
- Pragmatic style (120 chars) reduces unnecessary wrapping/churn.

### Negative

- Additional tooling to install locally.
- CI auto-fix does not change submitted code; developers still need local hooks to keep diffs clean.
