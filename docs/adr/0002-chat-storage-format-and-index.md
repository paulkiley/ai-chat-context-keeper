# 2. Chat Storage Format and Index

Date: 2025-09-03

## Status

Accepted

## Context

We need a simple, local-first way to persist chat history and retrieve the latest context segments by project/topic/session.

## Decision

Store chat chunks as Markdown files (`chat_history_00001.md`, ...). Maintain a JSON index (`chat_history_index.json`) with newest-first entries represented by a validated Pydantic model. Chunks store raw text; the index stores metadata for filtering.

## Consequences

### Positive

- Human-readable, easy to inspect and backup.
- Simple append/prepend operations on index.
- Efficient retrieval by metadata without scanning content.

### Negative

- No full-text search; future work may add indexing or external search.
- Large histories may require compaction/rotation policies later.
