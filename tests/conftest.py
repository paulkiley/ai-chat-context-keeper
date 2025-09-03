import os
import io
import pytest


@pytest.fixture()
def temp_history_dir(tmp_path, monkeypatch):
    # Patch the singleton settings to use an isolated temp directory
    from chat_history_manager import config

    base = tmp_path / "history"
    monkeypatch.setenv("CHAT_HISTORY_BASE_DIR", str(base))
    config.settings.CHAT_HISTORY_BASE_DIR = base
    return base


@pytest.fixture()
def stdin_text(monkeypatch):
    def _set(text: str):
        monkeypatch.setattr("sys.stdin", io.StringIO(text))
    return _set

