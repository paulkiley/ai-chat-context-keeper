from chat_history_manager.main import save_chat_history
from chat_history_manager.utils import read_chat_index


def test_retention_max_chunks(monkeypatch, temp_history_dir):
    # Keep only the latest 1 chunk
    monkeypatch.setenv("CHAT_RETENTION_MAX_CHUNKS", "1")
    # Re-import settings to pick up new env in this process
    from chat_history_manager import config

    config.settings.CHAT_RETENTION_MAX_CHUNKS = 1

    p1 = save_chat_history("conv-A", project_name="PZ", topic="T1", summary="S-A")
    p2 = save_chat_history("conv-B", project_name="PZ", topic="T2", summary="S-B")
    assert p1.exists() is False  # older file should be deleted
    assert p2.exists()

    idx = read_chat_index()
    assert len(idx) == 1
    assert idx[0].summary == "S-B"
