from chat_history_manager.config import Settings


def test_settings_interpolation_env(monkeypatch, tmp_path):
    # Use CHM_HISTORY_DIR via interpolation
    target = tmp_path / "hist"
    monkeypatch.setenv("CHM_HISTORY_DIR", str(target))
    s = Settings(CHAT_HISTORY_BASE_DIR="${CHM_HISTORY_DIR:-/unused}")
    assert s.CHAT_HISTORY_BASE_DIR == target
    assert s.CHAT_HISTORY_INDEX_FILE.name == "chat_history_index.json"
