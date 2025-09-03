# Kubernetes Integration

Secrets

- Use External Secrets Operator to sync cloud secrets to env or files.
- Map to environment variables consumed by this package (e.g., `CHAT_HISTORY_BASE_DIR`, custom `CHM_HISTORY_DIR`).

Example ExternalSecret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: chm-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: my-secret-store
    kind: ClusterSecretStore
  target:
    name: chm-app-secrets
  data:
    - secretKey: CHM_HISTORY_DIR
      remoteRef:
        key: /apps/chat-history-manager/history-dir
```

Example Deployment env

```yaml
env:
  - name: CHAT_HISTORY_BASE_DIR
    value: '${CHM_HISTORY_DIR:-/data/chat-history}'
  - name: CHAT_RETENTION_MAX_CHUNKS
    value: '1000'
```

Storage

- Mount a PersistentVolume at the path used by `CHAT_HISTORY_BASE_DIR`.
