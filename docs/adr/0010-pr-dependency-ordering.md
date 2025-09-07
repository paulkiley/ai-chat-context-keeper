# 10. pr dependency ordering

Date: 2025-09-07

## Status

Accepted

## Context

We enforce safe PR merge sequencing via a CI workflow () using a dependency map (.github/pr-deps.json). For scale, JSON can introduce merge hotspots; the designated scaling path is to parse "Depends-On: #<id>" PR body trailers and/or label-based groupings, and to publish a nightly dependency graph for visibility.

## Decision

\[Summarize the decision concisely.\]

## Consequences

\[List positive/negative tradeoffs.\]

## Metadata

- supersedes: \[\]
- depends_on: \[\]
- informs: \[\]

## Security & Privacy Considerations

\[Outline any implications; references to threat model if applicable.\]
