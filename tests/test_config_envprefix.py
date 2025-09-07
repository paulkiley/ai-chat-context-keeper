from chat_history_manager.config import Settings


def test_chm_history_base_dir_prefix(monkeypatch, tmp_path):
    base = tmp_path / "hist"
    monkeypatch.setenv("CHM_HISTORY_BASE_DIR", str(base))
    s = Settings()
    assert s.CHAT_HISTORY_BASE_DIR == base
