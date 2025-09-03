# 3. CLI Surface and VS Code Tasks

Date: 2025-09-03

## Status

Accepted

## Context

Developers need quick capture and retrieval flows during day-to-day work, including clipboard → log and terminal-first usage.

## Decision

Provide a Python console script `chatlog` with `save` and `retrieve` subcommands. Add VS Code tasks for saving clipboard content and retrieving filtered chunks, relying on environment-driven config.

## Consequences

### Positive

- Fast, scriptable workflows; minimal friction to log chats.
- Editor integration for common actions.

### Negative

- Editor-specific tasks need maintenance; CLI remains the stable surface.

