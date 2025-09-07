# Known Issues

Functional

- No full-text search; retrieval is metadata-based only.
- Index consistency: corruption recovery is best-effort (rebuild not yet implemented).
- Retention is best-effort; age pruning uses local time and may behave differently across timezones.

Concurrency

- File locks rely on `flock`/`fcntl` and may not work reliably on some network filesystems (e.g., certain NFS mounts). Consider local disk for history or stronger locking if used over network shares.

Security

- No encryption at rest; history and index are plaintext files.
- Keyring usage is optional; secrets are not required by this package today.
- No RBAC or multi-tenant isolation (single-user local tool).

Portability

- Windows support is untested for locking behavior; path defaults are set but need validation.

Performance

- Very large indices could degrade retrieval performance; compaction/rotation tooling is not yet implemented.
