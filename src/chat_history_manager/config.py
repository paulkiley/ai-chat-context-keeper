import os
import platform
import re
from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from .secrets_provider import default_provider

def _apply_env_compat() -> None:
    """Map new CHM_* variables to legacy names if legacy unset.

    - CHM_HISTORY_BASE_DIR -> CHAT_HISTORY_BASE_DIR
    - CHM_RETENTION_MAX_CHUNKS -> CHAT_RETENTION_MAX_CHUNKS
    - CHM_RETENTION_MAX_AGE_DAYS -> CHAT_RETENTION_MAX_AGE_DAYS
    - CHM_READ_ONLY -> READ_ONLY
    """
    mapping = {
        "CHM_HISTORY_BASE_DIR": "CHAT_HISTORY_BASE_DIR",
        "CHM_RETENTION_MAX_CHUNKS": "CHAT_RETENTION_MAX_CHUNKS",
        "CHM_RETENTION_MAX_AGE_DAYS": "CHAT_RETENTION_MAX_AGE_DAYS",
        "CHM_READ_ONLY": "READ_ONLY",
    }
    for src, dst in mapping.items():
        if src in os.environ and dst not in os.environ:
            os.environ[dst] = os.environ[src]

def _default_history_base_dir() -> Path:
    # Cross-platform sensible defaults with override via env
    system = platform.system().lower()
    xdg = os.environ.get("XDG_DATA_HOME")
    if system == "darwin":
        return Path.home() / "Library" / "Application Support" / "chat_history_manager" / "history"
    if system == "windows":
        return Path.home() / "AppData" / "Local" / "chat_history_manager" / "history"
    if xdg:
        return Path(xdg) / "chat_history_manager" / "history"
    return Path.home() / ".local" / "share" / "chat_history_manager" / "history"


VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)?(?::-([^}]*))?\}")


def _interpolate(text: str) -> str:
    """Interpolate ${VAR} or ${VAR:-default} from env or keyring.

    Order: env -> keyring; if unset and default provided, use default.
    """
    provider = default_provider()

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        if not name:
            return match.group(0)
        val = os.environ.get(name)
        if val is None:
            # Try keyring provider under the same key name
            val = provider.get(name)
        if val is None:
            val = default
        return val if val is not None else ""

    return VAR_PATTERN.sub(repl, text)


_apply_env_compat()


class Settings(BaseSettings):
    """
    Manages application settings using environment variables and a .env file.

    The base directory for chat history defaults to a hidden directory
    in the user's home folder, which is a robust cross-platform standard.
    """
    CHAT_HISTORY_BASE_DIR: Path = _default_history_base_dir()

    @property
    def CHAT_HISTORY_INDEX_FILE(self) -> Path:
        return self.CHAT_HISTORY_BASE_DIR / "chat_history_index.json"

    CHAT_CHUNK_SIZE: int = 4000

    # Optional retention policies (None = no limit)
    CHAT_RETENTION_MAX_CHUNKS: int | None = None
    CHAT_RETENTION_MAX_AGE_DAYS: int | None = None
    READ_ONLY: bool = False

    model_config = SettingsConfigDict(
        # Do not require or encourage committing .env; if present locally, it will be read.
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("CHAT_HISTORY_BASE_DIR", mode="before")
    @classmethod
    def expand_and_interpolate(cls, v: Any) -> Any:
        # Accept Path or string; interpolate ${...}, expand ~ and env vars.
        if isinstance(v, Path):
            s = str(v)
        else:
            s = str(v)
        s = _interpolate(s)
        s = os.path.expandvars(os.path.expanduser(s))
        return Path(s)

    @field_validator("READ_ONLY", mode="before")
    @classmethod
    def coerce_read_only(cls, v: Any) -> bool:
        # Accept True/False or string flags
        if isinstance(v, bool):
            return v
        val = str(v).lower()
        return val in {"1", "true", "yes", "on", "y", "t"}

settings = Settings()
