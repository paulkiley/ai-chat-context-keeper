import os
from typing import Optional, Sequence

try:
    import keyring  # type: ignore
except Exception:  # pragma: no cover
    keyring = None  # Optional dependency


class SecretProvider:
    def get(self, name: str) -> Optional[str]:  # pragma: no cover - interface
        raise NotImplementedError


class EnvSecretProvider(SecretProvider):
    def get(self, name: str) -> Optional[str]:
        return os.environ.get(name)


class KeyringSecretProvider(SecretProvider):
    def __init__(self, service: str = "chat_history_manager") -> None:
        self.service = service

    def get(self, name: str) -> Optional[str]:
        if keyring is None:
            return None
        try:
            # Use `name` as username within the service namespace
            return keyring.get_password(self.service, name)
        except Exception:
            return None


class ChainSecretProvider(SecretProvider):
    def __init__(self, providers: Sequence[SecretProvider]) -> None:
        self.providers = list(providers)

    def get(self, name: str) -> Optional[str]:
        for p in self.providers:
            val = p.get(name)
            if val is not None:
                return val
        return None


def default_provider() -> ChainSecretProvider:
    """Env first, then OS keychain if available."""
    service = os.environ.get("CHM_KEYRING_SERVICE", "chat_history_manager")
    providers: list[SecretProvider] = [EnvSecretProvider(), KeyringSecretProvider(service)]
    return ChainSecretProvider(providers)


def get_secret(name: str, provider: Optional[SecretProvider] = None) -> Optional[str]:
    prov = provider or default_provider()
    return prov.get(name)
