import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from .config import settings
from .models import IndexEntry


def ensure_chat_history_dir_exists():
    """Ensures the base directory for chat history exists."""
    settings.CHAT_HISTORY_BASE_DIR.mkdir(parents=True, exist_ok=True)


def get_next_chunk_number() -> int:
    """Determines the next available chunk number based on existing files."""
    ensure_chat_history_dir_exists()
    existing_chunks = [int(p.stem.split("_")[-1]) for p in settings.CHAT_HISTORY_BASE_DIR.glob("chat_history_*.md")]
    return max(existing_chunks) + 1 if existing_chunks else 1


def write_chat_chunk(chunk_number: int, content: str) -> Path:
    """Writes a chat chunk to a Markdown file."""
    ensure_chat_history_dir_exists()
    file_path = settings.CHAT_HISTORY_BASE_DIR / f"chat_history_{chunk_number:05d}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def read_chat_chunk(chunk_number: int) -> Optional[str]:
    """Reads a chat chunk from a Markdown file."""
    file_path = settings.CHAT_HISTORY_BASE_DIR / f"chat_history_{chunk_number:05d}.md"
    return file_path.read_text(encoding="utf-8") if file_path.exists() else None


def read_chat_index() -> List[IndexEntry]:
    """Reads and parses the JSON index file into a list of IndexEntry models."""
    index_path = settings.CHAT_HISTORY_INDEX_FILE
    if not index_path.exists():
        return []
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
        return [IndexEntry(**entry) for entry in data]
    except (json.JSONDecodeError, TypeError):
        return []


def update_chat_index(new_entry: IndexEntry):
    """Updates the chat history index file with a new entry."""
    ensure_chat_history_dir_exists()
    entries = read_chat_index()
    entry_dicts = [entry.model_dump(mode="json") for entry in entries]
    entry_dicts.insert(0, new_entry.model_dump(mode="json"))

    settings.CHAT_HISTORY_INDEX_FILE.write_text(json.dumps(entry_dicts, indent=4), encoding="utf-8")


def _write_index_entries(entries: List[IndexEntry]) -> None:
    entry_dicts = [entry.model_dump(mode="json") for entry in entries]
    settings.CHAT_HISTORY_INDEX_FILE.write_text(json.dumps(entry_dicts, indent=4), encoding="utf-8")


def extract_latest_conversation(full_conversation: str) -> str:
    """Extracts the latest characters from the full conversation."""
    return full_conversation[-settings.CHAT_CHUNK_SIZE :]


def get_current_datetime() -> datetime:
    """Returns the current datetime object."""
    return datetime.now()


try:
    import fcntl  # type: ignore
except Exception:  # pragma: no cover
    fcntl = None


class ChatHistoryLock:
    """Simple lock using flock where available, else create/unlink file.

    Ensures only one writer mutates the history at a time.
    """

    def __init__(self) -> None:
        ensure_chat_history_dir_exists()
        self.lock_path = settings.CHAT_HISTORY_BASE_DIR / ".chm.lock"
        self._fh = None  # type: ignore
        self._fd = None  # type: ignore

    def __enter__(self):
        if fcntl is not None:
            self._fh = open(self.lock_path, "w")
            fcntl.flock(self._fh, fcntl.LOCK_EX)
        else:
            # create exclusively; will fail if exists
            flags = os.O_CREAT | os.O_EXCL | os.O_RDWR
            self._fd = os.open(self.lock_path, flags, 0o644)
            os.write(self._fd, str(os.getpid()).encode())
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if fcntl is not None and self._fh is not None:
                fcntl.flock(self._fh, fcntl.LOCK_UN)
                self._fh.close()
            elif self._fd is not None:
                os.close(self._fd)
        finally:
            try:
                if self.lock_path.exists():
                    self.lock_path.unlink()
            except Exception:
                pass
        return False


def chat_history_lock() -> ChatHistoryLock:
    return ChatHistoryLock()


def apply_retention_policies() -> None:
    """Apply retention based on configuration.

    - CHAT_RETENTION_MAX_CHUNKS: keep only the most recent N chunks.
    - CHAT_RETENTION_MAX_AGE_DAYS: remove entries older than N days.
    """
    max_chunks = settings.CHAT_RETENTION_MAX_CHUNKS
    max_age_days = settings.CHAT_RETENTION_MAX_AGE_DAYS

    if max_chunks is None and max_age_days is None:
        return

    entries = read_chat_index()  # newest-first order
    now = get_current_datetime()
    cutoff = None
    if isinstance(max_age_days, int) and max_age_days > 0:
        cutoff = now - timedelta(days=max_age_days)

    # Determine which entries to keep
    to_keep: List[IndexEntry] = []
    for i, e in enumerate(entries):
        too_old = cutoff is not None and e.end_datetime < cutoff
        over_limit = isinstance(max_chunks, int) and max_chunks > 0 and i >= max_chunks
        if too_old or over_limit:
            continue
        to_keep.append(e)

    # Collect files that will be deleted
    keep_files = {e.file for e in to_keep}
    to_delete_files = [e.file for e in entries if e.file not in keep_files]

    # Delete files from disk
    for fname in to_delete_files:
        fpath = settings.CHAT_HISTORY_BASE_DIR / fname
        try:
            if fpath.exists():
                fpath.unlink()
        except Exception:
            # Best-effort deletion; continue
            pass

    # Rewrite index with kept entries
    _write_index_entries(to_keep)
