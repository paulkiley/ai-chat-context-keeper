# 1. Adopt 12-Factor Config and Secrets Chain

Date: 2025-09-03

## Status

Accepted

## Context

We must avoid repository-coupled personal configurations and secrets, while enabling portable development and CI/CD. Values should be provided at runtime and work across macOS, Linux, and Windows.

## Decision

Adopt an env-first configuration model with `${VAR}` and `${VAR:-default}` interpolation. Implement a secrets provider that resolves keys from environment variables first, then the OS keychain (`keyring`) for prototype-friendly development. Provide sensible per-OS defaults when not configured.

## Consequences

### Positive

- Clean repos with no personal configs or secrets.
- Portable setups and reproducible CI.
- Easy override in local shells and orchestrators.

### Negative

- Requires developers to set environment variables or keychain entries.
- Some complexity in interpolation logic and support.
